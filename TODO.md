# Fix Django Migration Error (Missing Google Auth Dependency)

**Status: Dependencies Fixed - Run migrations manually with venv active**

## Steps:
- [x] 1. Create requirements.txt in config/ ✅ (Done)
- [x] 2. cd config && pip install -r requirements.txt ✅ (Complete: google-auth installed)
- [ ] 3. python manage.py makemigrations  
- [ ] 4. python manage.py migrate
- [ ] 5. python manage.py runserver (test)
- [ ] 6. Test Google SSO login in browser (optional)

**Notes:**
- All Django commands from config/ dir with venv active.
- If mysqlclient fails on Windows: pip install PyMySQL and add 'PyMySQL' as DB engine in settings.py.
- Ensure MySQL server running with DB 'mechalocate_db', user 'mechauser'/pass '1234'.
- Venv activation: cd config && ..\\venv\\Scripts\\activate.bat (Windows cmd)
- Ensure MySQL server running ('mechalocate_db' DB)
- Add FAST2SMS_API_KEY to .env in project root.

