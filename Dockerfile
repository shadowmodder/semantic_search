# Use an official Ubuntu base image
FROM python:3.11
# RUN apt-get update && apt-get install -y python3 python3-pip
# Install Rust compiler
RUN apt-get update && apt-get install -y rustc
WORKDIR /app
COPY . .
EXPOSE 8080
# Make the run script executable
RUN chmod +x /app/entrypoint.sh
# Specify the Bash script as the entry point
ENTRYPOINT ["/app/entrypoint.sh"]