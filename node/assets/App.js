import { React, useState } from 'react'

import {
  Link
} from 'react-router-dom'


/**
 * Creates the omnipresent navbar for the site
 */
export function Header () {
    return (
        <section className='top-bar'>
            <div className='flex-container centered'>
                <section className='nav-area'>
                    <Link to='/newpage1' className='nav-item'>
                        Nav Link 1
                    </Link>
                </section>
            </div>
        </section>
    )
}

/**
 * Creates the main body content for the landing page
 */
export function Home () {
    return (
      <section>
        <h2>Hello</h2>
      </section>
    )
  }