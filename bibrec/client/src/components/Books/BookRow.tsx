import React from 'react'
import BookItem from './bookItem'
import "./Books.scss"

export default function BookRow() {
  return (
    <div className='bookRow'>
        {dummyBooks.map((book, index) => <BookItem key={index} title={book.title} imageURL={book.imageURL} rating={book.rating} author={book.author}/>)}
    </div>
  )
}

const dummyBooks = [
    {
    title:"Buchempfehlung", 
    imageURL:"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg", 
    author:"Autor", 
    rating:4.5
    },
    {
        title:"Buchempfehlung", 
        imageURL:"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg", 
        author:"Autor", 
        rating:4.5
    },
    {
        title:"Buchempfehlung", 
        imageURL:"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg", 
        author:"Autor", 
        rating:4.5
    },
    {
        title:"Buchempfehlung", 
        imageURL:"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg", 
        author:"Autor", 
        rating:4.5
    },
    {
        title:"Buchempfehlung", 
        imageURL:"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg", 
        author:"Autor", 
        rating:4.5
    }
]
