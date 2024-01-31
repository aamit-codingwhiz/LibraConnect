const form = document.getElementById('addBookForm');
const tableBody = document.querySelector('#booksTable tbody');
const totalBooksCountElement = document.getElementById('totalBooksCount');
let categoryContent = []


function fetchBooks() {
    fetch('http://127.0.0.1:5000/api/books')
        .then(response => response.json())
        .then(books => {
            tableBody.innerHTML = '';
            let countBook = 1;
            books.forEach(book => {
                categoryContent.push({title: book.title });

                const row = document.createElement('tr');
                row.innerHTML = `
                        <td>${countBook++}</td>
                        <td>${book.title}</td>
                        <td>${book.author}</td>
                        <td>${book.file_path ? `<a href="http://127.0.0.1:5000/${book.file_path}" target="_blank">Download</a>` : 'N/A'}</td>
                        <td>
                            <button class="ui red icon button" onclick="deleteBook(${book.id})">
                                <i class="trash icon"></i>
                            </button>
                        </td>
                    `;
                tableBody.appendChild(row);
            });

            totalBooksCountElement.textContent = books.length;
            $('.ui.search')
                .search({
                    source: categoryContent
                })
                ;
        });
}


function addBook(event) {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('title', title);
    formData.append('author', author);
    formData.append('file', file);

    try {
        fetch('http://127.0.0.1:5000/api/books', {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to add the book. Please try again.');
                }
                return response.json();
            })
            .then(() => {
                fetchBooks();
                form.reset();
            })
            .catch(error => {
                alert(`Error: ${error.message}`);
            });
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}


function deleteBook(bookId) {
    console.log('delete requested of book ' + bookId);
    try {
        fetch(`http://127.0.0.1:5000/api/books/${bookId}`, {
            method: 'DELETE'
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete the book. Please try again.');
                }
                return response.json();
            })
            .then(() => fetchBooks())
            .catch(error => {
                alert(`Error: ${error.message}`);
            });
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

form.addEventListener('submit', addBook);
fetchBooks();
