import React, { useState } from "react";
import BookDetailModal from "../components/BookDetails/BookDetailModal";
import { Book } from "../components/Books/BookItem";
import BookRow from "../components/Books/BookRow";
import "./Home.scss";

export default function Home() {
	const [modalVisible, setModalVisible] = useState(false);
	const [selectedBook, setSelectedBook] = useState<undefined | Book>(
		undefined
	);

	return (
		<div className="wrapper">
			{modalVisible && selectedBook ? (
				<BookDetailModal
					selectedBook={selectedBook}
					onClose={setModalVisible}
				/>
			) : null}
			<h2>Deine Empfehlungen</h2>
			<BookRow
				onItemClick={(book: Book) => {
					setModalVisible(true);
					setSelectedBook(book);
					console.log(book);
					
				}}
			/>
			<h2>Top 5 in deinem Land</h2>
			<BookRow
				onItemClick={(book: Book) => {
					setModalVisible(true);
					setSelectedBook(book);
				}}
			/>
			<h2>Mehr erkunden</h2>
			<BookRow
				onItemClick={(book: Book) => {
					setModalVisible(true);
					setSelectedBook(book);
				}}
			/>
			<button>Mehr laden</button>
		</div>
	);
}
