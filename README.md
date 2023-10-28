# Book Store Project in Django

## Project Description

This Django-based Book Store project is designed to provide an easy-to-use platform for managing and purchasing books. Key features include:

- Adding, deleting, and updating books, authors, and genres.
- User management with the ability to assign staff rights for book data manipulation.
- Adding books to a cart and making purchases (handled by creating a text file with purchase information).

## Getting Started

To run the Book Store locally, follow these steps:

1. Clone the repository:
```
git clone git@github.com:Dekrazi/Book-Store.git
```

2. Navigate to the project directory where the Makefile is located.

3. Use the following Make commands:

- `make run`: Install the requirements and start the application. 
- Then, go to `http://127.0.0.1:8000/` in your browser to access the project.

- `make clean`: Delete the virtual environment and clean cache.

### Additional Docker Commands

If you want to use Docker, use the following additional commands:

- `make docker-login`: Login to Docker Hub.
- `make docker-build`: Create a Docker image.
- `make docker-push`: Push the image to Docker Hub.
- `make docker-clean`: Remove the image locally.


## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Known Issues and Future Work

- Issues with displaying number of items in the cart on diferent website locations (JavaScript related)
