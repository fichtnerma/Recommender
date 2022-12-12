import React, { useState } from "react";
import BookDetailModal from "../components/BookDetails/BookDetailModal";
import { Book } from "../components/Books/BookItem";
import BookRow from "../components/Books/BookRow";
import "./Home.scss";
import { dummyBooks2 } from "../components/Books/mockData";
import { User } from "../App";

interface HomeProps {
	user?: User;
}

export default function Home({ user }: HomeProps) {
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
					user={user}
				/>
			) : null}
			{user ? <>
				<h2>Deine Empfehlungen</h2>
				<BookRow
					onItemClick={(book: Book) => {
						setModalVisible(true);
						setSelectedBook(book);
						console.log(book);

					}}
					books={dummyBooks2}/>
			</> : null}
			<h2>Top 5 in deinem Land</h2>
			<BookRow
				onItemClick={(book: Book) => {
					setModalVisible(true);
					setSelectedBook(book);
				}}
				books={dummyBooks2}/>
			<h2>Mehr erkunden</h2>
			<BookRow
				onItemClick={(book: Book) => {
					setModalVisible(true);
					setSelectedBook(book);
				}}
				books={dummyBooks2}/>
			<button>Mehr laden</button>
		</div>
	);
}
