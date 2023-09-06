# Use an official Ubuntu base image
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY . .
EXPOSE 8080
# Make the run script executable
RUN chmod +x install.sh
# Specify the Bash script as the entry point
ENTRYPOINT ["install.sh"]