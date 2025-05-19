#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User tracking module for the Telegram Chat Bot
Tracks user interactions and schedules re-engagement messages
"""

import time
import logging
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
import random

class UserTracker:
    def __init__(self):
        """Initialize the user tracker"""
        # Store user interaction data
        # Structure: {user_id: {'last_start': timestamp, 'clicked': bool, 'follow_up_sent': bool}}
        self.user_data = defaultdict(lambda: {'last_start': None, 'clicked': False, 'follow_up_sent': False})
        self.scheduled_tasks = {}  # Store scheduled follow-up tasks
        logging.info("UserTracker initialized")
    
    def track_start(self, user_id):
        """
        Track when a user starts the bot
        
        Args:
            user_id: The user's Telegram ID
        """
        self.user_data[user_id]['last_start'] = time.time()
        self.user_data[user_id]['clicked'] = False
        self.user_data[user_id]['follow_up_sent'] = False
        
        user_id_hash = hash(str(user_id)) % 10000
        logging.info(f"User start tracked for user_hash:{user_id_hash}")
        
    def track_click(self, user_id):
        """
        Track when a user clicks on a profile
        
        Args:
            user_id: The user's Telegram ID
            
        Returns:
            bool: True if this is the first click after starting, False otherwise
        """
        # Only mark as clicked if they started recently
        if self.user_data[user_id]['last_start'] is not None:
            was_clicked = self.user_data[user_id]['clicked']
            self.user_data[user_id]['clicked'] = True
            
            # Cancel any scheduled follow-up for this user
            self.cancel_scheduled_follow_up(user_id)
            
            user_id_hash = hash(str(user_id)) % 10000
            logging.info(f"Click tracked for user_hash:{user_id_hash}")
            
            # Return True only if this is the first click after starting
            return not was_clicked
            
        return False
    
    def needs_follow_up(self, user_id, elapsed_minutes=30):
        """
        Check if a user needs a follow-up message
        
        Args:
            user_id: The user's Telegram ID
            elapsed_minutes: Minutes since start to trigger follow-up
            
        Returns:
            bool: True if the user needs a follow-up, False otherwise
        """
        user_data = self.user_data[user_id]
        
        # If user hasn't started, clicked, or already got a follow-up, no need
        if (user_data['last_start'] is None or 
            user_data['clicked'] or 
            user_data['follow_up_sent']):
            return False
            
        # Check if enough time has elapsed
        elapsed = time.time() - user_data['last_start']
        return elapsed >= (elapsed_minutes * 60)
    
    def mark_follow_up_sent(self, user_id):
        """
        Mark that a follow-up was sent to the user
        
        Args:
            user_id: The user's Telegram ID
        """
        self.user_data[user_id]['follow_up_sent'] = True
        user_id_hash = hash(str(user_id)) % 10000
        logging.info(f"Follow-up marked as sent for user_hash:{user_id_hash}")
    
    def schedule_follow_up(self, user_id, callback, minutes=30):
        """
        Schedule a follow-up message for a user
        
        Args:
            user_id: The user's Telegram ID
            callback: Async function to call
            minutes: Minutes to wait before follow-up
        """
        # Cancel any existing follow-up for this user
        self.cancel_scheduled_follow_up(user_id)
        
        # Schedule the new follow-up
        task = asyncio.create_task(self._delayed_follow_up(user_id, callback, minutes))
        self.scheduled_tasks[user_id] = task
        
        user_id_hash = hash(str(user_id)) % 10000
        logging.info(f"Follow-up scheduled in {minutes} minutes for user_hash:{user_id_hash}")
    
    def cancel_scheduled_follow_up(self, user_id):
        """
        Cancel a scheduled follow-up for a user
        
        Args:
            user_id: The user's Telegram ID
        """
        if user_id in self.scheduled_tasks:
            task = self.scheduled_tasks.pop(user_id)
            task.cancel()
            user_id_hash = hash(str(user_id)) % 10000
            logging.info(f"Scheduled follow-up cancelled for user_hash:{user_id_hash}")
    
    async def _delayed_follow_up(self, user_id, callback, minutes):
        """
        Internal method to handle the delayed follow-up
        
        Args:
            user_id: The user's Telegram ID
            callback: Function to call
            minutes: Minutes to wait
        """
        try:
            # Wait for specified minutes
            await asyncio.sleep(minutes * 60)
            
            # Only send if the user still needs a follow-up
            if self.needs_follow_up(user_id):
                await callback(user_id)
                self.mark_follow_up_sent(user_id)
        except asyncio.CancelledError:
            # Task was cancelled, just pass
            pass
        except Exception as e:
            user_id_hash = hash(str(user_id)) % 10000
            logging.error(f"Error in follow-up for user_hash:{user_id_hash}: {e}")
        finally:
            # Remove the task from scheduled tasks if it's still there
            if user_id in self.scheduled_tasks:
                del self.scheduled_tasks[user_id]

# Create a global instance
user_tracker = UserTracker()
