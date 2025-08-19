import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className='header'>
      <nav className='nav navbar'>
        <div className='container'>
          <ul className='nav navbar-links'>
            <li className='nav-item'>
              <Link to="/">Home</Link>
            </li>
            <li className='nav-item'>
              <Link to="/new-job">New</Link>
            </li>
            <li className='nav-item'>
              <Link to="/search-jobs">Search</Link>
            </li>
            <li className='nav-item'>
              <Link to="/tools">Tools</Link>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  );
}

export default Header;