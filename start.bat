@echo off
chcp 65001 >nul
title Birthday Website Server
echo ====================================================
echo   تشغيل موقع عيد الميلاد ولوحة التحكم محليا
echo ====================================================
echo جاري تشغيل الخادم وفتح لوحة التحكم والموقع في المتصفح...
echo.
start http://localhost:8000/admin.html
start http://localhost:8000/index.html
echo.
echo الخادم يعمل الان على: http://localhost:8000
echo اي تعديل في لوحة التحكم سيتم حفظه تلقائيا في الملفات مباشرة!
echo اضغط Ctrl+C لايقاف الخادم.
echo ====================================================
python server.py
pause
