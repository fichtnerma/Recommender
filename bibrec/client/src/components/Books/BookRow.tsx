import React from "react";
import BookItem from "./BookItem";
import "./Books.scss";
import { Book } from "../../types/types";

interface BookRowProps {
	books: Book[];
	onItemClick: (value: Book) => void;
	limit?: number;
}

export default function BookRow({ onItemClick, books, limit = 5 }: BookRowProps) {
	return (
		<div className="bookRow">
			{books.slice(0, limit).map((book, index) => (
				<BookItem
					key={index}
					book={book}
					onItemClick={() => onItemClick(book)}
				/>
			))}
		</div>
	);
}
