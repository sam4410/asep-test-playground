   ("newuser", "newpass"),
   ("testuser", "testpass"),
   base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
   
   # Sign up
   page.goto(f"{base_url}/signup")
   page.fill("input[name='username']", username)
   page.fill("input[name='password']", password)
   page.click("text=Sign Up")
   page.wait_for_url(f"{base_url}/login")
   
   # Check if redirected to login
   assert "Log In" in page.content()
   
   # Log in
   page.fill("input[name='username']", username)
   page.fill("input[name='password']", password)
   page.click("text=Log In")
   page.wait_for_url(f"{base_url}/dashboard")
   
   # Check if redirected to dashboard
   assert "Dashboard" in page.content()
   base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
   
   # Log in first
   page.goto(f"{base_url}/login")
   page.fill("input[name='username']", "testuser")
   page.fill("input[name='password']", "testpass")
   page.click("text=Log In")
   page.wait_for_url(f"{base_url}/dashboard")
   
   # Log out
   page.click("text=Logout")
   page.wait_for_url(f"{base_url}/login")
   
   # Check if logged out
   assert "Log In" in page.content()