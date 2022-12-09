import React from "react";
import { Book } from "../Books/BookItem";
import Rating from "../Books/Rating";
import "./BookDetails.scss";

interface BookDetailsProps {
	selectedBook: Book;
}

export default function BookDetails({ selectedBook }: BookDetailsProps) {
	const { imageURL, author, rating, title } = selectedBook;

	return (
		<div className="bookDetails">
			<img src={imageURL} alt={`The cover for the book „${title}“`} />
			<Rating rating={+rating} />
			<span>123 Bewertungen</span>
			<h2>{title}</h2>
			<h3>{author}</h3>
			<p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem amet. Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem amet. Quod.</p>
		</div>
	);
}
