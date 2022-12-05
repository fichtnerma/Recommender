import React from 'react'
import "./Books.scss"
import Rating from './Rating'

interface Book {
    title: string,
    imageURL: string,
    author: string,
    rating: number
}

export default function BookItem({title, imageURL, author, rating} : Book) {
  return (
    <div className='bookItem element'>
        <img src={imageURL} alt="book cover"/>
        <h3>{title}</h3>
        <p>{author}</p>
        <Rating rating={+rating}/>
    </div>
  )
}
