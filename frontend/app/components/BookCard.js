import Link from 'next/link';
import styles from '../../styles/BookCard.module.css';

const BookCard = ({ book }) => (
  <div className={styles.wrapper}>
    {/* 제목을 URL 인코딩하여 상세 페이지로 링크 */}
    <Link href={`/book/${encodeURIComponent(book.title)}`} legacyBehavior>
      <a className={styles.card}> {/* Link 내부에 <a> 태그 추가 */}
        <div className={styles.imageWrapper}>
          <img src={book.image} alt={book.title} />
        </div>
        <h3 className={styles.title}>{book.title}</h3> {/* 제목 */}
      </a>
    </Link>
  </div>
);

export default BookCard;
