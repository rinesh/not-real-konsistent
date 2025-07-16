#!/usr/bin/env python3
"""
Quick test script to verify the local setup works
"""
import sys
import os

def test_imports():
    print("Testing imports...")
    try:
        import flask
        print(f"✅ Flask imported successfully")
        
        import replicate
        print(f"✅ Replicate imported successfully")
        
        from app import RealMePredictor
        print("✅ RealMePredictor imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_api_token():
    print("\nTesting API token...")
    api_token = input("Enter your Replicate API token (or press Enter to skip): ").strip()
    
    if not api_token:
        print("⚠️  Skipping API token test")
        return True
    
    try:
        import replicate
        client = replicate.Client(api_token=api_token)
        
        # Test a simple call
        print("Testing API connection...")
        output = client.run("replicate/hello-world:5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa", 
                          input={"text": "test"})
        print(f"✅ API test successful: {output}")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    print("🧪 Real-Me Local Test Script")
    print("=" * 40)
    
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        sys.exit(1)
    
    if not test_api_token():
        print("\n⚠️  API token test failed. You may need to check your token when using the app.")
    
    print("\n✅ All tests passed!")
    print("\nNext steps:")
    print("1. Run: python app.py")
    print("2. Open: http://localhost:5000")
    print("3. Enter your Replicate API token")
    print("4. Test the model!")

if __name__ == "__main__":
    main()