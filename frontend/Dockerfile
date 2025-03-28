FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Set environment variables
ENV NODE_ENV=production

# Build the app
RUN npm run build

# Start the app
CMD ["npm", "start"]