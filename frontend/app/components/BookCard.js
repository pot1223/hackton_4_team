import Link from 'next/link';
import styles from '../../styles/BookCard.module.css';

const BookCard = ({ book }) => (
  <div className={styles.wrapper}>
    <Link href={`/book/${book.id}`}>
      <div className={styles.card}>
        <div className={styles.imageWrapper}>
          <img src={book.image} alt={book.title} />
        </div>
        <h3 className={styles.title}>{book.title}</h3> {/* 제목 */}
      </div>
    </Link>
  </div>
);

export default BookCard;