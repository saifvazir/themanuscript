-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 05, 2016 at 08:52 AM
-- Server version: 10.1.16-MariaDB
-- PHP Version: 5.5.38

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `TheManuscript`
--

-- --------------------------------------------------------

--
-- Table structure for table `Books`
--

CREATE TABLE `Books` (
  `Book_id` varchar(20) NOT NULL,
  `Title` varchar(50) NOT NULL,
  `Genre` varchar(100) NOT NULL,
  `Coverpage` longblob NOT NULL,
  `Tags` varchar(50) NOT NULL,
  `Content_id` varchar(30) NOT NULL,
  `Author_id` varchar(30) NOT NULL,
  `Story_type` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Count`
--

CREATE TABLE `Count` (
  `userscount` int(30) NOT NULL,
  `bookscount` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Count`
--

INSERT INTO `Count` (`userscount`, `bookscount`) VALUES
(5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `Example`
--

CREATE TABLE `Example` (
  `id` int(12) NOT NULL,
  `data` varchar(322) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Example`
--

INSERT INTO `Example` (`id`, `data`) VALUES
(1, 'ewffw'),
(2, 'ankitesh');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`id`, `name`, `password`) VALUES
(1, 'ankitesh', 'gupta');

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `User_id` varchar(20) NOT NULL,
  `Username` varchar(30) NOT NULL,
  `Email_id` varchar(30) NOT NULL,
  `Password` varchar(30) DEFAULT NULL,
  `Profile_pic` longblob,
  `Age` datetime DEFAULT NULL,
  `Languages` varchar(60) DEFAULT NULL,
  `Location` varchar(30) DEFAULT NULL,
  `Genres` varchar(60) DEFAULT NULL,
  `Dateentry` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`User_id`, `Username`, `Email_id`, `Password`, `Profile_pic`, `Age`, `Languages`, `Location`, `Genres`, `Dateentry`) VALUES
('#UOBJ14', 'ankityifscesrdegf', 'ankdwfwe', 'c99a11a53a3748269e3f86d7ac38df', NULL, NULL, NULL, NULL, NULL, '2016-12-04 15:08:50'),
('#UOBJ15', 'ankitesdh97', 'ankdwfwe', 'c99a11a53a3748269e3f86d7ac38df', NULL, NULL, NULL, NULL, NULL, '2016-12-04 15:45:06'),
('#UOBJ71', 'ankifgf', 'ankdwfwe', 'c99a11a53a3748269e3f86d7ac38df', NULL, NULL, NULL, NULL, NULL, '2016-12-04 14:05:58'),
('#UOBJ81', 'ankitesh97', 'ankiteshguptas@gmail.com', '3537460fefa4597153b1f493524efe', NULL, NULL, NULL, NULL, NULL, '2016-12-04 08:18:22'),
('#UOBJ91', 'ankitesh9', 'ankiteshguptas@gmail.com', '63efba8c48eae1e816e0dd969d6811', NULL, NULL, NULL, NULL, NULL, '2016-12-04 11:07:18');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Books`
--
ALTER TABLE `Books`
  ADD PRIMARY KEY (`Book_id`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD UNIQUE KEY `User_id` (`User_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
