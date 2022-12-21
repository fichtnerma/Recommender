import React, { useEffect, useState } from "react";
import BookDetails from "./BookDetails";
import { User } from "../../App";
import BookRow from "../Books/BookRow";
import axios from "axios";
import LoadingIndicator from "../Utils/LoadingIndicator";
import { Book, Rating } from "../../types/types";

interface BookDetailModelProps {
	selectedBook: Book;
	onClose: (value: boolean) => void;
	setSelectedBook: (value: Book) => void;
	user?: User;
	userRatings: Rating[];
	setUserRatings: (value: Rating[]) => void;
}

export default function BookDetailModal(props: BookDetailModelProps) {
	const {
		onClose,
		selectedBook,
		user,
		setSelectedBook,
		setUserRatings,
		userRatings
	} = props;

	const [similarBooks, setSimilarBooks] = useState<Book[]>([]);

	useEffect(() => {
		document.addEventListener("keydown", handleCloseOnEsc);
		getSimilarBooks(selectedBook.isbn);

		return () => document.removeEventListener("keydown", handleCloseOnEsc);
	}, []);

	function getSimilarBooks(isbn10: string) {
		try {
			axios.post("http://localhost:4000/similarBooks", {
				userId: user?.id,
				isbn10,
				recommendationCount: 5
			}).then((res) => {
				setSimilarBooks(res.data);
			});

		} catch (e) {
			console.error(e);
		}
	}

	function handleCloseOnEsc(e: KeyboardEvent) {
		e.code === "Escape" && onClose(false);
	}

	function onRate(selectedRating: number) {
		const sendRating = confirm(`Möchtest du das Buch „${selectedBook.book_title}“ wirklich mit ${selectedRating} Sternen bewerten?`);
		if (sendRating) {
			try {
				if (!user) return;
				axios.post("http://localhost:4000/ratings", {
					userId: user.id,
					isbn10: selectedBook.isbn,
					rating: selectedRating
				}).then(() => {
					const { rating_count, rating_mean } = selectedBook;
					const updatedCount = rating_count + 1;
					const updatedMean = (rating_count * rating_mean + 1 * selectedRating) / (rating_count + 1);
					setSelectedBook({ ...selectedBook, rating_count: updatedCount, rating_mean: updatedMean });
				}).then(() => {
					axios.get("http://localhost:4000/ratings", { params: { userId: user.id } })
						.then((res) => {
							setUserRatings(res.data);
							console.log(res.data);
						});
				});


			} catch (e) {
				console.error(e);
			}
		}
	}

	return (
		<div className="modalBackground">
			<div className="detailModal">
				<div className={"closeIcon"} onClick={() => onClose(false)}/>
				<BookDetails selectedBook={selectedBook} user={user} onRate={onRate}
							 userRating={userRatings.find(rating => rating.isbn === selectedBook.isbn)}/>
				<div>
					<h2>Diese Bücher könnten dir auch gefallen</h2>

					{similarBooks?.length
						? <BookRow books={similarBooks} onItemClick={(book) => {
							setSelectedBook(book);
							setSimilarBooks([])
							getSimilarBooks(book.isbn);
						}}/>
						: <LoadingIndicator/>
					}
				</div>
			</div>
		</div>
	);
}
