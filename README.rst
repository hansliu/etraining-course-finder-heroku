eTraining Course Finder
=======================

What is etraining-course-finder
-------------------------------

因為勞動部勞動力發展署網站實在太難用，所以自己開發一個好用的網站。

實作上採用的是 Python3 搭配 Flask 架構。

在課程資料來源的部份，使用 Selenium 收集勞動部勞動力發展署網站公開的課程資料（目前收集的課程範圍只有臺北市和新北市），然後將課程資料建置索引之後儲存於 Sqlite3 的資料庫中。

目前的功能：

#. 直覺式的課程尋找. (暫時限定: 臺北市, 新北市)
#. 顯示課程資訊、課程的報名時間與開訓時間。
#. 顯示課程代碼，可以連結到相關課程的詳細介紹頁面。

Build up course.db in yourself platform
---------------------------------------

Run model.py directly

::

  # build up db
  cd etraining-course-finder-heroku/
  python3.* ./etraining_course_finder/model.py

  # update db to github
  git pull ; git add -u ; git commit -m'updated db' ; git push

Save the commands to script, and run build up course.db by cronjob

::

  # edit cronjob
  crontab -e

  # setup schedule for your script
  HOME=/home/<your_account>
  1 6 * * 1 <your_script> &> /dev/null

Build up etraining-course-finder in Heroku
------------------------------------------

Refer: http://tech.pro/tutorial/1259/how-to-deploy-simple-and-larger-flask-apps-on-heroku

::

  cd etraining-course-finder-heroku/
  virtualenv venv
  . venv/bin/activate
  pip install Flask
  pip install gunicorn
  pip freeze > requirements.txt
  cat 'web: gunicorn etraining_course_finder:app' > Procfile

Because XVFB issue in Heroku, you should build up course.db in yourself platform

Config file for Heroku

+ Procfile
+ requirements.txt
+ runtime.txt

Config file for Flask

+ publishconf.py
