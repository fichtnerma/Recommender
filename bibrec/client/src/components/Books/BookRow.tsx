import React from "react";
import BookItem, { Book } from "./BookItem";
import "./Books.scss";

interface BookRowProps {
	onItemClick: (value: Book) => void;
}

export default function BookRow({ onItemClick }: BookRowProps) {
	return (
		<div className="bookRow">
			{dummyBooks2.map((book, index) => (
				<BookItem
					key={index}
					title={book.title}
					imageURL={book.imageURL}
					rating={book.rating}
					author={book.author}
					onItemClick={() => onItemClick(book)}
				/>
			))}
		</div>
	);
}

const dummyBooks = [
	{
		title: "Buchempfehlung",
		imageURL:
			"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg",
		author: "Autor",
		rating: 4,
	},
	{
		title: "Buchempfehlung",
		imageURL:
			"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg",
		author: "Autor",
		rating: 8.5,
	},
	{
		title: "Buchempfehlung",
		imageURL:
			"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg",
		author: "Autor",
		rating: 6.25,
	},
	{
		title: "Buchempfehlung",
		imageURL:
			"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg",
		author: "Autor",
		rating: 2.75,
	},
	{
		title: "Buchempfehlung",
		imageURL:
			"https://100covers4you.com/wp-content/uploads/2022/03/20220320_151244-768x1229.jpg",
		author: "Autor",
		rating: 4.5,
	},
];

const dummyBooks2 = [
	{
		id: "0393045218",
		title: "The Mummies of Urumchi",
		author: "E. J. W. Barber",
		pubYear: "1999",
		publisher: "W. W. Norton &amp Company",
		imageURL:
			"http://images.amazon.com/images/P/0393045218.01.LZZZZZZZ.jpg",
		rating: 6,
	},
	{
		id: "0679777431",
		title: "The Game of Kings (Lymond Chronicles, 1)",
		author: "DOROTHY DUNNETT",
		pubYear: "1997",
		publisher: "Vintage",
		imageURL:
			"http://images.amazon.com/images/P/0679777431.01.LZZZZZZZ.jpg",
		rating: 8,
	},
	{
		id: "0753804700",
		title: "Reader",
		author: "Bernhard Schlink",
		pubYear: "0",
		publisher: "Phoenix Books",
		imageURL:
			"http://images.amazon.com/images/P/0753804700.01.LZZZZZZZ.jpg",
		rating: 3,
	},
	{
		id: "0679772677",
		title: "A Civil Action",
		author: "JONATHAN HARR",
		pubYear: "1996",
		publisher: "Vintage",
		imageURL:
			"http://images.amazon.com/images/P/0679772677.01.LZZZZZZZ.jpg",
		rating: 9,
	},
	{
		id: "0679732241",
		title: "The Sound and the Fury (Vintage International)",
		author: "WILLIAM FAULKNER",
		pubYear: "1991",
		publisher: "Vintage",
		imageURL:
			"http://images.amazon.com/images/P/0679732241.01.LZZZZZZZ.jpg",
		rating: 10,
	},
];
