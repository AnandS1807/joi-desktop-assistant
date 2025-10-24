import pyautogui
import time
import subprocess
import os
import json
import psutil
from datetime import datetime
from pathlib import Path

class WorkflowExecutor:
    def __init__(self):
        self.pyautogui = pyautogui
        self.pyautogui.FAILSAFE = True
        self.pyautogui.PAUSE = 1.0  # Increased pause for reliability
        
    def execute_workflow(self, workflow_data):
        """Execute a detected workflow"""
        workflow_name = workflow_data.get('workflow_name', '')
        print(f"🤖 Executing workflow: {workflow_name}")
        
        try:
            # Add a safety delay
            print("⏳ Starting automation in 3 seconds...")
            time.sleep(3)
            
            if 'excel' in workflow_name:
                return self._execute_excel_workflow(workflow_data)
            elif 'word' in workflow_name:
                return self._execute_word_workflow(workflow_data)
            elif 'explorer' in workflow_name:
                return self._execute_explorer_workflow(workflow_data)
            elif 'chrome' in workflow_name:
                return self._execute_chrome_workflow(workflow_data)
            else:
                print(f"❓ Unknown workflow type: {workflow_name}")
                return False
                
        except Exception as e:
            print(f"❌ Workflow execution failed: {e}")
            return False
    
    def _execute_excel_workflow(self, workflow_data):
        """Execute Excel-related workflows"""
        workflow_name = workflow_data['workflow_name']
        
        if 'opening' in workflow_name:
            return self._open_excel()
            
        elif 'creating' in workflow_name or 'formula' in workflow_name:
            if self._open_excel():
                time.sleep(5)  # Wait for Excel to fully load
                return self._create_excel_budget()
            
        return False
    
    def _open_excel(self):
        """Open Excel using multiple methods"""
        print("📱 Attempting to open Excel...")
        
        # Method 1: Try Windows Run dialog
        try:
            self.pyautogui.hotkey('win', 'r')
            time.sleep(1)
            self.pyautogui.write('excel')
            self.pyautogui.press('enter')
            time.sleep(5)
            
            # Check if Excel opened by looking for Excel window
            if self._is_application_open('Excel'):
                print("✅ Excel opened successfully via Run dialog")
                return True
        except Exception as e:
            print(f"❌ Excel Run dialog method failed: {e}")
        
        # Method 2: Try Start Menu search
        try:
            self.pyautogui.hotkey('win')
            time.sleep(1)
            self.pyautogui.write('excel')
            time.sleep(2)
            self.pyautogui.press('enter')
            time.sleep(5)
            
            if self._is_application_open('Excel'):
                print("✅ Excel opened successfully via Start Menu")
                return True
        except Exception as e:
            print(f"❌ Excel Start Menu method failed: {e}")
        
        # Method 3: Try direct command
        try:
            subprocess.Popen('excel', shell=True)
            time.sleep(5)
            
            if self._is_application_open('Excel'):
                print("✅ Excel opened successfully via command")
                return True
        except Exception as e:
            print(f"❌ Excel command method failed: {e}")
        
        print("❌ All Excel opening methods failed")
        return False
    
    def _create_excel_budget(self):
        """Create a simple budget in Excel"""
        try:
            print("💰 Creating Excel budget...")
            
            # Wait a bit more for Excel to be ready
            time.sleep(3)
            
            # Create title
            self.pyautogui.write('Monthly Budget')
            self.pyautogui.press('enter')
            self.pyautogui.press('down')
            
            # Create headers
            self.pyautogui.write('Category')
            self.pyautogui.press('tab')
            self.pyautogui.write('Amount')
            self.pyautogui.press('enter')
            self.pyautogui.press('down')
            
            # Add data
            categories = ['Revenue', 'Expenses', 'Profit']
            amounts = ['50000', '30000', '=B2-B3']
            
            for i, (category, amount) in enumerate(zip(categories, amounts)):
                self.pyautogui.write(category)
                self.pyautogui.press('tab')
                self.pyautogui.write(amount)
                if i < len(categories) - 1:
                    self.pyautogui.press('enter')
                    self.pyautogui.press('down')
            
            print("✅ Excel budget created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Excel budget creation failed: {e}")
            return False
    
    def _execute_word_workflow(self, workflow_data):
        """Execute Word workflows"""
        workflow_name = workflow_data['workflow_name']
        
        if 'opening' in workflow_name:
            return self._open_word()
            
        elif 'creating' in workflow_name or 'writing' in workflow_name:
            if self._open_word():
                time.sleep(5)
                return self._create_word_document()
            
        return False
    
    def _open_word(self):
        """Open Word using multiple methods"""
        print("📝 Attempting to open Word...")
        
        # Method 1: Windows Run dialog
        try:
            self.pyautogui.hotkey('win', 'r')
            time.sleep(1)
            self.pyautogui.write('winword')
            self.pyautogui.press('enter')
            time.sleep(5)
            
            if self._is_application_open('Word'):
                print("✅ Word opened successfully via Run dialog")
                return True
        except Exception as e:
            print(f"❌ Word Run dialog method failed: {e}")
        
        # Method 2: Start Menu
        try:
            self.pyautogui.hotkey('win')
            time.sleep(1)
            self.pyautogui.write('word')
            time.sleep(2)
            self.pyautogui.press('enter')
            time.sleep(5)
            
            if self._is_application_open('Word'):
                print("✅ Word opened successfully via Start Menu")
                return True
        except Exception as e:
            print(f"❌ Word Start Menu method failed: {e}")
        
        print("❌ All Word opening methods failed")
        return False
    
    def _create_word_document(self):
        """Create a simple Word document"""
        try:
            print("📄 Creating Word document...")
            time.sleep(3)
            
            # Write document content
            self.pyautogui.write('Automated Document')
            self.pyautogui.press('enter')
            self.pyautogui.press('enter')
            
            self.pyautogui.write('This document was created automatically by the AI Assistant.')
            self.pyautogui.press('enter')
            self.pyautogui.press('enter')
            
            self.pyautogui.write('Created on: ')
            self.pyautogui.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            print("✅ Word document created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Word document creation failed: {e}")
            return False
    
    def _execute_explorer_workflow(self, workflow_data):
        """Execute File Explorer workflows"""
        try:
            print("📁 Opening File Explorer...")
            self.pyautogui.hotkey('win', 'e')
            time.sleep(3)
            
            # Navigate to Documents
            self.pyautogui.write('documents')
            time.sleep(1)
            self.pyautogui.press('enter')
            time.sleep(2)
            
            print("✅ File Explorer workflow completed!")
            return True
            
        except Exception as e:
            print(f"❌ File Explorer workflow failed: {e}")
            return False
    
    def _execute_chrome_workflow(self, workflow_data):
        """Execute Chrome workflows"""
        try:
            print("🌐 Opening Chrome...")
            subprocess.Popen('chrome', shell=True)
            time.sleep(5)
            
            # Search for something
            self.pyautogui.write('AI automation tools')
            self.pyautogui.press('enter')
            time.sleep(2)
            
            print("✅ Chrome workflow completed!")
            return True
            
        except Exception as e:
            print(f"❌ Chrome workflow failed: {e}")
            return False
    
    def _is_application_open(self, app_name):
        """Check if an application is currently running"""
        app_name_lower = app_name.lower()
        for process in psutil.process_iter(['name']):
            try:
                if app_name_lower in process.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    
    def test_basic_automation(self):
        """Test basic automation capabilities safely"""
        print("🧪 Testing basic automation...")
        
        print("⏳ Test starting in 5 seconds...")
        time.sleep(5)
        
        try:
            # Test 1: Simple typing
            print("⌨️ Testing typing...")
            self.pyautogui.write('Automation Test - Hello World!')
            time.sleep(1)
            
            # Test 2: Press enter
            print("↵ Testing enter key...")
            self.pyautogui.press('enter')
            time.sleep(1)
            
            # Test 3: Open Run dialog
            print("🪟 Testing Run dialog...")
            self.pyautogui.hotkey('win', 'r')
            time.sleep(1)
            self.pyautogui.press('esc')  # Close it
            
            print("✅ Basic automation test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Basic automation test failed: {e}")
            return False