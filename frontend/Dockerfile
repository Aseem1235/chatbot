FROM node:18

WORKDIR /app

# Copy only package.json and package-lock.json first (for caching)
COPY ./package*.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . /app/

# Build the React app
RUN npm run build

# Use `serve` to host the production build
RUN npm install -g serve
CMD ["serve", "-s", "build"]
