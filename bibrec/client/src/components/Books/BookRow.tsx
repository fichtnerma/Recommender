import React from "react";
import BookItem, { Book } from "./BookItem";
import "./Books.scss";
import { dummyBooks2 } from "./mockData";

interface BookRowProps {
	books: Book[];
	onItemClick: (value: Book) => void;
}

export default function BookRow({ onItemClick, books }: BookRowProps) {
	return (
		<div className="bookRow">
			{books.map((book, index) => (
				<BookItem
					key={index}
					title={book.title}
					imageURL={book.imageURL}
					rating={book.rating}
					author={book.author}
					onItemClick={() => onItemClick(book)}
				/>
			))}
		</div>
	);
}

