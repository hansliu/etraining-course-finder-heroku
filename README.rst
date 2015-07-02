eTraining Course Finder
=======================

What is etraining-course-finder
-------------------------------

因為勞動部勞動力發展署網站實在太難用，所以自己開發一個好用的網站頁面。

使用 Selenium 收集勞動部勞動力發展署網站公開的課程資料（目前收集的課程範圍只有臺北市和新北市），然後將課程資料建置索引之後儲存於 Sqlite3 的資料庫中。

目前的功能：

#. 直覺式的課程尋找. (暫時限定: 臺北市, 新北市)
#. 顯示課程資訊、課程的報名時間與開訓時間。
#. 顯示課程代碼，可以連結到相關課程的詳細介紹頁面。

Build up etraining-course-finder in Heroku
------------------------------------------

refer: http://tech.pro/tutorial/1259/how-to-deploy-simple-and-larger-flask-apps-on-heroku

::

  cd etraining-course-finder-heroku/
  virtualenv venv
  . venv/bin/activate
  pip install Flask
  pip install gunicorn
  pip freeze > requirements.txt
  cat 'web: gunicorn routes:app' > Procfile

Config file for Heroku

+ Procfile
+ requirements.txt
+ runtime.txt
