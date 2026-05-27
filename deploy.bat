@echo off
echo [1/3] Cleaning and Generating...
call hexo clean
call hexo g
echo [2/3] Entering public folder...
cd public
git init
git add .
git commit -m "Update Blog: %date% %time%"
echo [3/3] Forcing push to GitHub...
git push -f https://github.com/2829750658t-svg/2829750658t-svg.github.io.git master:main
echo Done! Your blog is now online.
pause