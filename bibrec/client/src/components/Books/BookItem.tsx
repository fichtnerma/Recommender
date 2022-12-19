import React from "react";
import "./Books.scss";
import Rating from "./Rating";

interface BookItemProps {
	onItemClick: (value: boolean) => void;
	book: Book;
}

export interface Book {
	isbn10: string;
	isbn13: number;
	title: string;
	imageUrlLarge: string;
	imageUrlMedium: string;
	imageUrlSmall: string;
	author: string;
	rating_count: number;
	rating_mean: number;
	pubYear: number;
	publisher: string;
}

export default function BookItem({ book, onItemClick }: BookItemProps) {
	const { title, rating_mean, imageUrlMedium, author } = book;

	return (
		<div className="bookItem element" onClick={() => onItemClick(true)}>
			<img src={imageUrlMedium} alt={`The cover for the book „${title}“`}/>
			<Rating rating={+rating_mean}/>
			<h3 className="bookTitle">{title}</h3>
			<span>{author}</span>
		</div>
	);
}
