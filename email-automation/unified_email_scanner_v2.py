#!/usr/bin/env python3
"""
Unified Email Scanner v2
- Reads unseen emails, classifies based on subject
- Learns from existing email folders to improve classification
- Modular design for different email types (employment, coupons, etc.)
"""

import imaplib
import email
import email.policy
import re
import datetime
import os
import sys
import ssl
import json
import pickle
from email.header import decode_header
from collections import defaultdict
import hashlib
from pathlib import Path

# ============================================================================
# Configuration
# ============================================================================

class Config:
    """Configuration for Proton Bridge and scanner settings."""
    
    # Proton Bridge IMAP settings
    IMAP_HOST = 'localhost'
    IMAP_PORT = 1143
    
    # Training folders for employment emails
    # These folders contain labeled examples for learning
    EMPLOYMENT_TRAINING_FOLDERS = {
        'rejected': 'Folders/01 - 1 Jobs/01 - New Work Search/rejected',
        'app_confirmed': 'Folders/01 - 1 Jobs/01 - New Work Search/APP CONF',
        'more_info': 'Folders/01 - 1 Jobs/01 - New Work Search/still in process',
    }
    
    # Output folders for classified emails
    OUTPUT_FOLDERS = {
        'rejected': 'Folders/0 - AI/0 AI - Jobs/ToBeChecked - R',
        'app_confirmed': '',  # Leave in INBOX
        'more_info': '',      # Leave in INBOX
        'unknown_employment': '',  # Leave in INBOX
    }
    
    # Model storage
    MODEL_FILE = os.path.expanduser('~/.openclaw/email_classifier.model')
    
    # Minimum confidence threshold for classification (0.0-1.0)
    MIN_CONFIDENCE = 0.6
    
    @staticmethod
    def get_credentials():
        """Get Proton Bridge credentials from config file."""
        config_path = os.path.expanduser('~/.config/openclaw/proton_bridge.env')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Proton Bridge config not found at {config_path}")
        
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith('PROTON_IMAP_USER='):
                    email_addr = line.split('=', 1)[1].strip().strip('"')
                elif line.startswith('PROTON_IMAP_PASSWORD='):
                    password = line.split('=', 1)[1].strip().strip('"')
        
        return email_addr, password

# ============================================================================
# Email Learning Classifier
# ============================================================================

class EmailClassifier:
    """Learns from email folders and classifies new emails."""
    
    def __init__(self, model_file=None):
        self.model_file = model_file or Config.MODEL_FILE
        self.model = {
            'folder_profiles': {},  # folder_name -> {word: frequency}
            'total_emails': 0,
            'updated_at': None
        }
        self.load_model()
    
    def load_model(self):
        """Load trained model from file."""
        if os.path.exists(self.model_file):
            try:
                with open(self.model_file, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"Loaded classifier model from {self.model_file}")
                print(f"  Model trained on {self.model['total_emails']} emails")
                print(f"  Last updated: {self.model.get('updated_at', 'unknown')}")
            except Exception as e:
                print(f"Warning: Could not load model: {e}")
                self.model = {'folder_profiles': {}, 'total_emails': 0, 'updated_at': None}
        else:
            print("No existing model found. Will train from folders.")
    
    def save_model(self):
        """Save trained model to file."""
        os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
        with open(self.model_file, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Saved classifier model to {self.model_file}")
    
    def extract_features(self, subject, body=None):
        """Extract features from email subject and body."""
        text = subject.lower()
        if body:
            text += " " + body.lower()
        
        # Simple word tokenization (improve as needed)
        words = re.findall(r'\b[a-z]{3,15}\b', text)
        
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'you', 'your', 'have', 'with', 'this', 'that', 'are', 'from'}
        words = [w for w in words if w not in stop_words]
        
        # Count frequencies
        features = defaultdict(int)
        for word in words:
            features[word] += 1
        
        return features
    
    def train_from_folder(self, imap_connection, folder_path, label):
        """Train classifier from emails in a specific folder."""
        print(f"Training from folder '{folder_path}' as label '{label}'...")
        
        try:
            status, count = imap_connection.select(f'"{folder_path}"')
            if status != 'OK':
                print(f"  Warning: Could not select folder {folder_path}: {count}")
                return 0
            
            total_msgs = int(count[0])
            if total_msgs == 0:
                print(f"  No emails in folder")
                return 0
            
            # Search for all emails
            status, msg_ids = imap_connection.search(None, 'ALL')
            if status != 'OK':
                print(f"  Could not search folder: {msg_ids}")
                return 0
            
            msg_ids = msg_ids[0].split()
            processed = 0
            
            # Initialize profile for this label if not exists
            if label not in self.model['folder_profiles']:
                self.model['folder_profiles'][label] = defaultdict(int)
            
            profile = self.model['folder_profiles'][label]
            
            # Sample up to 50 emails from folder (for speed)
            sample_size = min(50, len(msg_ids))
            sample_ids = msg_ids[:sample_size]
            
            for msg_id in sample_ids:
                try:
                    # Fetch subject and snippet of body
                    status, msg_data = imap_connection.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)] BODY.PEEK[TEXT])')
                    if status != 'OK':
                        continue
                    
                    # Parse email
                    msg = email.message_from_bytes(msg_data[0][1], policy=email.policy.default)
                    subject = msg.get('Subject', '')
                    
                    # Get body text (first 1000 chars)
                    body = ''
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_content()[:1000]
                                break
                    else:
                        body = msg.get_content()[:1000]
                    
                    # Extract features and add to profile
                    features = self.extract_features(subject, body)
                    for word, count in features.items():
                        profile[word] += count
                    
                    processed += 1
                    
                except Exception as e:
                    print(f"  Error processing email {msg_id}: {e}")
                    continue
            
            print(f"  Processed {processed} emails for label '{label}'")
            return processed
            
        except Exception as e:
            print(f"  Error training from folder {folder_path}: {e}")
            return 0
    
    def train_all_folders(self, imap_connection):
        """Train classifier from all configured training folders."""
        print("\n" + "="*60)
        print("Training classifier from email folders...")
        print("="*60)
        
        total_processed = 0
        for label, folder_path in Config.EMPLOYMENT_TRAINING_FOLDERS.items():
            processed = self.train_from_folder(imap_connection, folder_path, label)
            total_processed += processed
        
        self.model['total_emails'] = total_processed
        self.model['updated_at'] = datetime.datetime.now().isoformat()
        
        if total_processed > 0:
            self.save_model()
            print(f"\nTraining complete: {total_processed} emails processed")
        else:
            print("\nWarning: No training data collected")
        
        return total_processed
    
    def classify(self, subject, body=None):
        """Classify an email based on subject and optional body."""
        features = self.extract_features(subject, body)
        
        if not self.model['folder_profiles']:
            return 'unknown', 0.0
        
        scores = {}
        for label, profile in self.model['folder_profiles'].items():
            score = 0
            for word, count in features.items():
                score += profile.get(word, 0)
            scores[label] = score
        
        # Normalize scores
        total = sum(scores.values())
        if total == 0:
            return 'unknown', 0.0
        
        best_label = max(scores.items(), key=lambda x: x[1])[0]
        confidence = scores[best_label] / total
        
        if confidence < Config.MIN_CONFIDENCE:
            return 'unknown', confidence
        
        return best_label, confidence

# ============================================================================
# Email Router
# ============================================================================

class EmailRouter:
    """Routes emails to appropriate handlers based on classification."""
    
    def __init__(self, imap_connection, classifier):
        self.imap = imap_connection
        self.classifier = classifier
    
    def process_unseen_emails(self):
        """Process all unseen emails in INBOX."""
        print("\n" + "="*60)
        print("Processing unseen emails...")
        print("="*60)
        
        # Select INBOX
        status, count = self.imap.select('INBOX')
        if status != 'OK':
            print(f"Error selecting INBOX: {count}")
            return 0
        
        # Search for unseen emails
        status, unseen_data = self.imap.search(None, 'UNSEEN')
        if status != 'OK' or not unseen_data[0]:
            print("No unseen emails found")
            return 0
        
        unseen_ids = unseen_data[0].split()
        print(f"Found {len(unseen_ids)} unseen emails")
        
        processed = 0
        for msg_id in unseen_ids:
            try:
                processed += self.process_single_email(msg_id)
            except Exception as e:
                print(f"Error processing email {msg_id}: {e}")
                continue
        
        print(f"\nProcessed {processed} emails")
        return processed
    
    def process_single_email(self, msg_id):
        """Process a single email by ID."""
        # Fetch full email
        status, msg_data = self.imap.fetch(msg_id, '(RFC822)')
        if status != 'OK':
            print(f"  Error fetching email {msg_id}")
            return 0
        
        # Parse email
        msg = email.message_from_bytes(msg_data[0][1], policy=email.policy.default)
        subject = msg.get('Subject', '')
        from_addr = msg.get('From', '')
        
        print(f"\nProcessing email {msg_id}:")
        print(f"  From: {from_addr}")
        print(f"  Subject: {subject[:80]}...")
        
        # Get body text
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_content()[:2000]
                    break
        else:
            body = msg.get_content()[:2000]
        
        # Classify email
        label, confidence = self.classifier.classify(subject, body)
        
        print(f"  Classification: {label} (confidence: {confidence:.2f})")
        
        # Route based on classification
        self.route_email(msg_id, msg, label, confidence)
        
        return 1
    
    def route_email(self, msg_id, msg, label, confidence):
        """Move email to appropriate folder based on classification."""
        if label == 'unknown' or confidence < Config.MIN_CONFIDENCE:
            print(f"  Action: Leaving in INBOX (low confidence)")
            return
        
        # Get destination folder
        dest_folder = Config.OUTPUT_FOLDERS.get(label)
        if not dest_folder:
            # Empty string means leave in INBOX
            return
        
        # Copy email to destination folder
        try:
            print(f"  Action: Moving to folder '{dest_folder}'")
            
            # IMAP COPY command
            status, response = self.imap.copy(msg_id, f'"{dest_folder}"')
            if status == 'OK':
                # Mark original for deletion (or just leave it)
                # self.imap.store(msg_id, '+FLAGS', '\\Deleted')
                print(f"  Success: Email copied to {dest_folder}")
            else:
                print(f"  Error copying email: {response}")
        
        except Exception as e:
            print(f"  Error moving email: {e}")

# ============================================================================
# Main Scanner
# ============================================================================

class UnifiedEmailScanner:
    """Main scanner orchestrator."""
    
    def __init__(self):
        self.imap = None
        self.classifier = None
        self.router = None
    
    def connect(self):
        """Connect to Proton Bridge IMAP server."""
        print("Connecting to Proton Bridge...")
        
        try:
            email_addr, password = Config.get_credentials()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Please create ~/.config/openclaw/proton_bridge.env with credentials")
            return False
        
        try:
            # Connect with plain IMAP then STARTTLS
            imap = imaplib.IMAP4(Config.IMAP_HOST, Config.IMAP_PORT)
            imap.starttls()
            imap.login(email_addr, password)
            
            self.imap = imap
            print("Connected successfully!")
            return True
            
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from IMAP server."""
        if self.imap:
            try:
                self.imap.logout()
                print("Disconnected from IMAP server")
            except:
                pass
    
    def run(self, mode='process'):
        """
        Run the scanner.
        
        Args:
            mode: 'train' - train classifier from folders
                  'process' - process unseen emails (default)
                  'both' - train then process
        """
        if not self.connect():
            print("Cannot continue without connection")
            return
        
        try:
            # Initialize classifier
            self.classifier = EmailClassifier()
            
            if mode in ['train', 'both']:
                # Train classifier
                self.classifier.train_all_folders(self.imap)
            
            if mode in ['process', 'both']:
                # Initialize router and process emails
                self.router = EmailRouter(self.imap, self.classifier)
                self.router.process_unseen_emails()
        
        finally:
            self.disconnect()

# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Unified Email Scanner v2')
    parser.add_argument('--mode', choices=['train', 'process', 'both'], default='process',
                       help='Operation mode: train classifier, process emails, or both')
    parser.add_argument('--list-folders', action='store_true',
                       help='List all available folders and exit')
    
    args = parser.parse_args()
    
    scanner = UnifiedEmailScanner()
    
    if args.list_folders:
        if scanner.connect():
            try:
                status, folders = scanner.imap.list()
                if status == 'OK':
                    print("Available folders:")
                    for folder in folders:
                        print(f"  {folder.decode()}")
            finally:
                scanner.disconnect()
        return
    
    scanner.run(mode=args.mode)

if __name__ == '__main__':
    main()