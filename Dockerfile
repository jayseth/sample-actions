# Use the official .NET SDK image as a base image
FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents to the container at /app
COPY . .

# Build the application
RUN dotnet publish -c Release -o out

# Use a lighter base image for the runtime
FROM mcr.microsoft.com/dotnet/runtime:5.0

# Set the working directory to /app
WORKDIR /app

# Copy the published output from the build image to the runtime image
COPY --from=build /app/out .

# Specify the entry point for the container
ENTRYPOINT ["dotnet", "sample-actions.dll"]
