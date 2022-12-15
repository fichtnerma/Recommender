import React from "react";
import { Book } from "../Books/BookItem";
import Rating from "../Books/Rating";
import "./BookDetails.scss";
import BookRow from "../Books/BookRow";
import { dummyBooks } from "../Books/mockData";
import { User } from "../../App";

interface BookDetailsProps {
	selectedBook: Book;
	setSelectedBook: (value: Book) => void;
	user?: User;
}

export default function BookDetails({ selectedBook, user, setSelectedBook }: BookDetailsProps) {
	const { imageURL, author, rating, title, pubYear } = selectedBook;

	return (
		<div className="bookDetails">
			<div className={"imageWrapper"}>
				<img src={imageURL} alt={`The cover for the book „${title}“`}/>
				<Rating rating={+rating} book={selectedBook}/>
				<span>123 Bewertungen</span>
			</div>

			<div className={"detailContent"}>
				<h2>{title}</h2>
				<h3>von {author}</h3>
				<h3>{pubYear}</h3>
				<p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt,
					atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem
					amet.
					Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae
					voluptatem amet. Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor
					explicabo possimus ipsam
					incidunt,
					atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem
					amet.
					Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae
					voluptatem amet.
				</p>
			</div>

			{!!user ? <div className="ratingCTA">
				<h3>Jetzt bewerten</h3>
				<Rating user={user} rating={0} book={selectedBook} canRate={true}/>
			</div> : null}
			<div>
				<h2>Diese Bücher könnten dir auch gefallen</h2>
				<BookRow books={dummyBooks} onItemClick={setSelectedBook}/>
			</div>
		</div>
	);
}
