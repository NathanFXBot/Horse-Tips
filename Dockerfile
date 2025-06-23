# Use official Node.js 18 image
FROM node:18

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN npm install

# Start the app
CMD ["node", "index.js"]
