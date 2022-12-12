import React from "react";
import BookItem, { Book } from "./BookItem";
import "./Books.scss";

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
					book={book}
					onItemClick={() => onItemClick(book)}
				/>
			))}
		</div>
	);
}

