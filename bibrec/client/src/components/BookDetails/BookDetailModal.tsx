import React, { useEffect, useState } from "react";
import { Book } from "../Books/BookItem";
import BookDetails from "./BookDetails";
import { User } from "../../App";
import BookRow from "../Books/BookRow";
import axios from "axios";
import LoadingIndicator from "../Utils/LoadingIndicator";

interface BookDetailModelProps {
	selectedBook: Book;
	onClose: (value: boolean) => void;
	setSelectedBook: (value: Book) => void;
	user?: User;
}

export default function BookDetailModal({ onClose, selectedBook, user, setSelectedBook }: BookDetailModelProps) {
	const [similarItems, setSimilarItems] = useState<Book[]>();

	useEffect(() => {
		document.addEventListener("keydown", handleCloseOnEsc);
		getSimilarBooks(selectedBook.isbn10);

		return () => document.removeEventListener("keydown", handleCloseOnEsc);
	}, []);

	function getSimilarBooks(isbn10: string) {
		try {
			axios.post("http://localhost:4000/similarBooks", {
				userId: user?.id,
				isbn10,
				recommendationCount: 5
			}).then((res) => {
				setSimilarItems(res.data);
			});

		} catch (e) {
			console.error(e);
		}
	}

	function handleCloseOnEsc(e: KeyboardEvent) {
		e.code === "Escape" && onClose(false);
	}

	return (
		<div className="modalBackground">
			<div className="detailModal">
				<div className={"closeIcon"} onClick={() => onClose(false)}/>
				<BookDetails selectedBook={selectedBook} setSelectedBook={setSelectedBook} user={user}/>
				<div>
					<h2>Diese Bücher könnten dir auch gefallen</h2>

					{similarItems?.length
						? <BookRow books={similarItems} onItemClick={(book) => {
							setSelectedBook(book);
							getSimilarBooks(book.isbn10);
						}}/>
						: <LoadingIndicator/>
					}
				</div>
			</div>
		</div>
	);
}
