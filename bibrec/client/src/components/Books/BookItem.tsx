import React from "react";
import "./Books.scss";
import Rating from "./Rating";

interface BookItemProps {
	onItemClick: (value: boolean) => void;
}

export interface Book {
	title: string;
	imageURL: string;
	author: string;
	rating: number;
}

export default function BookItem({
	title,
	imageURL,
	author,
	rating,
	onItemClick,
}: BookItemProps & Book) {
	return (
		<div className="bookItem element" onClick={() => onItemClick(true)}>
			<img  src={imageURL} alt={`The cover for the book „${title}“`} />
			<Rating rating={+rating} />
			<h3 className="bookTitle">{title}</h3>
			<span>{author}</span>
		</div>
	);
}
