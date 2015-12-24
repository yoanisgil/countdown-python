# countdown

I started this projet as a way to learn the [Flask Micro Framework](http://flask.pocoo.org/)

It allows users to create and share "countdowns" to a given date in a very simple way.

# Setup

All it takes are three simple steps:

  docker-compose build countdown # Build the application image
  docker-compose up -d countdown # Launch the application
  docker exec  rsyslog tail -f /var/log/messages # Monitor application logs
  
You might need to change the syslog server address, depending on your Docker setup. 
  

