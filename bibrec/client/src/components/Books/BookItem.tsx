import React from "react";
import "./Books.scss";
import Rating from "./Rating";

interface BookItemProps {
	onItemClick: (value: boolean) => void;
	book: Book;
}

export interface Book {
	title: string;
	imageURL: string;
	author: string;
	rating: number;
	pubYear: number;
	publisher: string;
}

export default function BookItem({ book, onItemClick }: BookItemProps) {
	const { title, rating, imageURL, author } = book;

	return (
		<div className="bookItem element" onClick={() => onItemClick(true)}>
			<img src={imageURL} alt={`The cover for the book „${title}“`}/>
			<Rating rating={+rating} book={book}/>
			<h3 className="bookTitle">{title}</h3>
			<span>{author}</span>
		</div>
	);
}
