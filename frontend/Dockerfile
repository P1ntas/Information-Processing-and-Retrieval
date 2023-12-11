# Use an official Node runtime as a parent image
FROM node:20-slim

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the current directory contents into the container at /app
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV REACT_APP_API_URL http://127.0.0.1:5000

# Build the React app
RUN npm run build

# Run the React app when the container launches
CMD ["npm", "start"]