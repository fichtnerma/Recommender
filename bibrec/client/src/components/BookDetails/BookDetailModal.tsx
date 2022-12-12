import React, { useEffect } from "react";
import { Book } from "../Books/BookItem";
import BookDetails from "./BookDetails";
import { User } from "../../App";

interface BookDetailModelProps {
	selectedBook: Book;
	onClose: (value: boolean) => void;
	user?: User;
}

export default function BookDetailModal({ onClose, selectedBook, user }: BookDetailModelProps) {

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
				<BookDetails selectedBook={selectedBook} user={user}/>
			</div>
		</div>
	);
}
