import React, { useState } from "react";
import { User } from "../../App";
import { Book } from "../Books/BookItem";
import BookDetails from "./BookDetails";

interface BookDetailModelProps {
	selectedBook: Book;
	onClose: (value: boolean) => void;
}
export default function BookDetailModal({ onClose, selectedBook }: BookDetailModelProps) {
	return (
		<div className="modalBackground">
			<div className="detailModal">
				<BookDetails selectedBook={selectedBook} />
				<button onClick={() => onClose(false)}>Schließen</button>
			</div>
		</div>
	);
}
