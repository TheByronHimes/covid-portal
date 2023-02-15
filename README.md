<h1>FastAPI & MongoDB Template with React</h1>
Use this to quickly start a single-page app with FastAPI and MongoDB through Docker.
<br>
<h2>Instructions</h2>
<ol>
<li>Clone the repo, then add a .env file to the top-level directory.
<li>In the .env file, add the two following lines, replacing "your_stuff_here" with your values:
<li>db_username=your_stuff_here
<li>db_password=your_stuff_here
<li>When you build the docker image file, it will pull in your authentication values and bake them in the image while keeping them out of your repo.
<li>Make sure you have Docker Desktop installed, then open a terminal and navigate to the repo folder.
<li>Build the image/run the containers with "docker-compose up --build".
<li>Open your browser and navigate to 127.0.0.1:8000, and you should see {"msg":"Hello World!"}
</ol>

You can build out the application from there.
