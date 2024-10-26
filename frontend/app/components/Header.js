import Link from 'next/link';
import styles from '../../styles/Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <Link href="/">
        <h1 style={{ color: 'white', paddingLeft: '32px' }}>담책</h1>
      </Link>
    </header>
  );
}