import React from "react";
import "./Books.scss";
import RatingStars from "./RatingStars";
import { Book } from "../../types/types";

interface BookItemProps {
	onItemClick: (value: boolean) => void;
	book: Book;
}

export default function BookItem({ book, onItemClick }: BookItemProps) {
	const { title, rating_mean, imageUrlMedium, author } = book;

	return (
		<div className="bookItem element" onClick={() => onItemClick(true)}>
			<img src={imageUrlMedium} alt={`The cover for the book „${title}“`}/>
			<RatingStars rating={+rating_mean}/>
			<h3 className="bookTitle">{title}</h3>
			<span>{author}</span>
		</div>
	);
}
