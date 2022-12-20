import React from "react";
import "./Books.scss";
import RatingStars from "./RatingStars";
import { Book } from "../../types/types";

interface BookItemProps {
	onItemClick: (value: boolean) => void;
	book: Book;
}

export default function BookItem({ book, onItemClick }: BookItemProps) {
	const { book_title, rating_mean, image_url_l, book_author } = book;

	return (
		<div className="bookItem element" onClick={() => onItemClick(true)}>
			<img src={image_url_l} alt={`The cover for the book „${book_title}“`}/>
			<RatingStars rating={+rating_mean}/>
			<h3 className="bookTitle">{book_title}</h3>
			<span>{book_author}</span>
		</div>
	);
}
