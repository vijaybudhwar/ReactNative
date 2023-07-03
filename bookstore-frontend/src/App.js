import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [books, setBooks] = useState([]);
    const [searchKeyword, setSearchKeyword] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    useEffect(() => {
        fetchBooks();
    }, []);

    const fetchBooks = async() => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/books');
            console.log(response.data); // Check the received data in the console
            setBooks(response.data);
        } catch (error) {
            console.error('Error fetching books:', error);
        }
    };

    const handleSearch = async() => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/api/books/search?q=${searchKeyword}`);
            setSearchResults(response.data);
        } catch (error) {
            console.error('Error searching books:', error);
        }
    };

    return ( <
        div className = "App" >
        <
        h1 > Online Bookstore < /h1> <
        div >
        <
        input type = "text"
        placeholder = "Search by title, author, or genre"
        value = { searchKeyword }
        onChange = {
            (e) => setSearchKeyword(e.target.value)
        }
        /> <
        button onClick = { handleSearch } > Search < /button> < /
        div > <
        div className = "book-list" > {
            searchResults.length > 0 ?
            searchResults.map((book) => ( <
                div key = { book.id }
                className = "book-card" >
                <
                img src = { book.cover_image_url }
                alt = { book.title }
                /> <
                h3 > { book.title } < /h3> <
                p > Author: { book.author } < /p> <
                p > Genre: { book.genre } < /p> <
                p > Price: $ { book.price } < /p> < /
                div >
            )) : books.map((book) => ( <
                div key = { book.id }
                className = "book-card" >
                <
                img src = { book.cover_image_url }
                alt = { book.title }
                /> <
                h3 > { book.title } < /h3> <
                p > Author: { book.author } < /p> <
                p > Genre: { book.genre } < /p> <
                p > Price: $ { book.price } < /p> < /
                div >
            ))
        } <
        /div> < /
        div >
    );
}

export default App;