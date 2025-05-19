#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rate limiting module to prevent bot abuse
"""

import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_calls=5, time_frame=60):
        """
        Initialize a rate limiter
        
        Args:
            max_calls: Maximum number of calls allowed in the time frame
            time_frame: Time frame in seconds
        """
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.user_calls = defaultdict(list)
        
    def is_allowed(self, user_id):
        """
        Check if a user is allowed to make a request
        
        Args:
            user_id: The ID of the user making the request
            
        Returns:
            bool: True if the user is allowed, False otherwise
        """
        current_time = time.time()
        
        # Remove old timestamps
        self.user_calls[user_id] = [
            timestamp for timestamp in self.user_calls[user_id] 
            if current_time - timestamp < self.time_frame
        ]
        
        # Check if the user has exceeded the rate limit
        if len(self.user_calls[user_id]) >= self.max_calls:
            return False
            
        # Add the current timestamp to the user's calls
        self.user_calls[user_id].append(current_time)
        return True
