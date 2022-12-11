import React, { useEffect } from "react";
import { Book } from "../Books/BookItem";
import BookDetails from "./BookDetails";

interface BookDetailModelProps {
	selectedBook: Book;
	onClose: (value: boolean) => void;
}

export default function BookDetailModal({ onClose, selectedBook }: BookDetailModelProps) {

	useEffect(() => {
		document.addEventListener("keydown", handleCloseOnEsc);

		return () => document.removeEventListener("keydown", handleCloseOnEsc);
	}, []);

	function handleCloseOnEsc(e: KeyboardEvent) {
		e.code === "Escape" && onClose(false);
	}

	return (
		<div className="modalBackground">
			<div className="detailModal">
				<div className={"closeIcon"} onClick={() => onClose(false)}/>
				<BookDetails selectedBook={selectedBook}/>
			</div>
		</div>
	);
}
