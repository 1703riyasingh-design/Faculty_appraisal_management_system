-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 15, 2026 at 01:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `appraisal_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `acr_approval`
--

CREATE TABLE `acr_approval` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `total_marks` float DEFAULT NULL,
  `grade` varchar(20) DEFAULT NULL,
  `hod_remark` text DEFAULT NULL,
  `principal_remark` text DEFAULT NULL,
  `hod_status` varchar(20) DEFAULT 'Pending',
  `principal_status` varchar(20) DEFAULT 'Pending',
  `submitted_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `percentage` float DEFAULT NULL,
  `responsibility` int(11) DEFAULT NULL,
  `punctuality` int(11) DEFAULT NULL,
  `commitment` int(11) DEFAULT NULL,
  `teamwork` int(11) DEFAULT NULL,
  `relationship` int(11) DEFAULT NULL,
  `hod_total` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `acr_approval`
--

INSERT INTO `acr_approval` (`id`, `faculty_id`, `total_marks`, `grade`, `hod_remark`, `principal_remark`, `hod_status`, `principal_status`, `submitted_at`, `percentage`, `responsibility`, `punctuality`, `commitment`, `teamwork`, `relationship`, `hod_total`) VALUES
(1, 1, 50853, 'Excellent', NULL, NULL, 'Rejected', 'Pending', '2026-02-09 21:26:55', 10170.6, NULL, NULL, NULL, NULL, NULL, NULL),
(2, 1, 50853, 'Excellent', NULL, NULL, 'Rejected', 'Pending', '2026-02-11 16:25:47', 10170.6, NULL, NULL, NULL, NULL, NULL, NULL),
(3, 1, 50853, 'Excellent', NULL, NULL, 'Rejected', 'Pending', '2026-02-11 16:25:53', 10170.6, NULL, NULL, NULL, NULL, NULL, NULL),
(4, 1, 50853, 'Excellent', NULL, NULL, 'Approved', 'Pending', '2026-02-11 16:53:15', 10170.6, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `faculty_id` int(11) DEFAULT NULL,
  `lab_dev` int(11) DEFAULT NULL,
  `dept_activity` int(11) DEFAULT NULL,
  `fdp` int(11) DEFAULT NULL,
  `research_guidance` int(11) DEFAULT NULL,
  `publications` int(11) DEFAULT NULL,
  `total_c` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `faculty_profile`
--

CREATE TABLE `faculty_profile` (
  `faculty_id` int(11) NOT NULL,
  `email` text DEFAULT NULL,
  `designation` text DEFAULT NULL,
  `department` text DEFAULT NULL,
  `qualification` text DEFAULT NULL,
  `specialization` text DEFAULT NULL,
  `dob` text DEFAULT NULL,
  `joining_date` text DEFAULT NULL,
  `phone` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faculty_profile`
--

INSERT INTO `faculty_profile` (`faculty_id`, `email`, `designation`, `department`, `qualification`, `specialization`, `dob`, `joining_date`, `phone`) VALUES
(1, '1703.2riyasingh@gmail.com', 'prof', 'btech', 'phd', 'artificial intelligence', '2001-01-06', '2026-02-01', '9340567542'),
(4, 'shibu@college.com', 'Assistent Professor', 'btech', 'PHD', 'Data Science', '1994-02-02', '2024-04-01', '987654321');

-- --------------------------------------------------------

--
-- Table structure for table `section_a_projects`
--

CREATE TABLE `section_a_projects` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `btech` int(11) DEFAULT 0,
  `mtech` int(11) DEFAULT 0,
  `mca_mba` int(11) DEFAULT 0,
  `papers` int(11) DEFAULT 0,
  `total_projects` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_a_projects`
--

INSERT INTO `section_a_projects` (`id`, `faculty_id`, `btech`, `mtech`, `mca_mba`, `papers`, `total_projects`) VALUES
(6, 1, 5, 4, 6, 15, 20);

-- --------------------------------------------------------

--
-- Table structure for table `section_a_workload`
--

CREATE TABLE `section_a_workload` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `course` varchar(50) DEFAULT NULL,
  `semester_section` varchar(50) DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  `subject_type` varchar(20) DEFAULT NULL,
  `scheduled_classes` int(11) DEFAULT NULL,
  `held_classes` int(11) DEFAULT NULL,
  `points` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_a_workload`
--

INSERT INTO `section_a_workload` (`id`, `faculty_id`, `course`, `semester_section`, `subject_name`, `subject_type`, `scheduled_classes`, `held_classes`, `points`) VALUES
(4, 1, 'btech', '2', 'JAVA', 'Theory', 40, 38, 78),
(6, 4, 'Btech', '5-a', 'DS', 'Practical', 25, 22, 10);

-- --------------------------------------------------------

--
-- Table structure for table `section_b_feedback`
--

CREATE TABLE `section_b_feedback` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `course` varchar(50) DEFAULT NULL,
  `semester_section` varchar(50) DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  `feedback_index` float DEFAULT NULL,
  `avg_feedback` float DEFAULT NULL,
  `session_type` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_b_feedback`
--

INSERT INTO `section_b_feedback` (`id`, `faculty_id`, `course`, `semester_section`, `subject_name`, `feedback_index`, `avg_feedback`, `session_type`) VALUES
(1, 1, 'MCA', '2', 'JAVA', 18, 18, 'Even'),
(2, 1, 'MCA', '2', 'JAVA', 18, 18, 'Even');

-- --------------------------------------------------------

--
-- Table structure for table `section_b_mentoring`
--

CREATE TABLE `section_b_mentoring` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `mentoring_details` text DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_b_mentoring`
--

INSERT INTO `section_b_mentoring` (`id`, `faculty_id`, `mentoring_details`, `marks`) VALUES
(1, 1, 'Mentored 25 students for academic improvement  Conducted monthly mentoring meetings  Career guidance sessions organized  Attendance monitoring and counseling', 8),
(2, 1, 'Mentored 25 students for academic improvement  Conducted monthly mentoring meetings  Career guidance sessions organized  Attendance monitoring and counseling', 8),
(3, 1, 'Mentored 25 students for academic improvement  Conducted monthly mentoring meetings  Career guidance sessions organized  Attendance monitoring and counseling', 8);

-- --------------------------------------------------------

--
-- Table structure for table `section_b_records`
--

CREATE TABLE `section_b_records` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `lesson_plan` tinyint(1) DEFAULT NULL,
  `question_bank` tinyint(1) DEFAULT NULL,
  `attendance_register` tinyint(1) DEFAULT NULL,
  `assignments` tinyint(1) DEFAULT NULL,
  `course_notes` tinyint(1) DEFAULT NULL,
  `lab_records` tinyint(1) DEFAULT NULL,
  `lab_manual` tinyint(1) DEFAULT NULL,
  `pedagogy_initiative` tinyint(1) DEFAULT NULL,
  `class_test_copies` tinyint(1) DEFAULT NULL,
  `action_taken` tinyint(1) DEFAULT NULL,
  `total_marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_b_records`
--

INSERT INTO `section_b_records` (`id`, `faculty_id`, `lesson_plan`, `question_bank`, `attendance_register`, `assignments`, `course_notes`, `lab_records`, `lab_manual`, `pedagogy_initiative`, `class_test_copies`, `action_taken`, `total_marks`) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 8),
(2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 40),
(3, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 45),
(4, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 45);

-- --------------------------------------------------------

--
-- Table structure for table `section_b_result`
--

CREATE TABLE `section_b_result` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `course` varchar(50) DEFAULT NULL,
  `semester_section` varchar(50) DEFAULT NULL,
  `subject_name` varchar(100) DEFAULT NULL,
  `result_percentage` float DEFAULT NULL,
  `avg_result` float DEFAULT NULL,
  `session_type` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_b_result`
--

INSERT INTO `section_b_result` (`id`, `faculty_id`, `course`, `semester_section`, `subject_name`, `result_percentage`, `avg_result`, `session_type`) VALUES
(1, 1, 'MCA', '2', 'JAVA', 7, 7, 'Odd'),
(2, 1, 'MCA', '2', 'JAVA', 7, 7, 'Odd'),
(3, 1, 'MCA', '2', 'JAVA', 7, 7, 'Odd');

-- --------------------------------------------------------

--
-- Table structure for table `section_c_department_activity`
--

CREATE TABLE `section_c_department_activity` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `activity_details` text DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_c_department_activity`
--

INSERT INTO `section_c_department_activity` (`id`, `faculty_id`, `activity_details`, `marks`) VALUES
(1, 1, 'Handled NAAC Documentation for Department\r\n', 24);

-- --------------------------------------------------------

--
-- Table structure for table `section_c_fdp`
--

CREATE TABLE `section_c_fdp` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `programme_name` varchar(255) DEFAULT NULL,
  `duration` varchar(100) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `institute_name` varchar(255) DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_c_fdp`
--

INSERT INTO `section_c_fdp` (`id`, `faculty_id`, `programme_name`, `duration`, `role`, `institute_name`, `marks`) VALUES
(1, 1, 'Completed 5-Day FDP on Machine Learning (AICTE Approved)', '5days', 'Organized', 'BIT-Durg', 15);

-- --------------------------------------------------------

--
-- Table structure for table `section_c_lab_development`
--

CREATE TABLE `section_c_lab_development` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `initiative` text DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_c_lab_development`
--

INSERT INTO `section_c_lab_development` (`id`, `faculty_id`, `initiative`, `marks`) VALUES
(1, 1, 'Prepared complete Lab Manual for DBMS practical\r\n', 10);

-- --------------------------------------------------------

--
-- Table structure for table `section_c_publications`
--

CREATE TABLE `section_c_publications` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `title` text DEFAULT NULL,
  `co_author` text DEFAULT NULL,
  `journal_name` text DEFAULT NULL,
  `category` varchar(10) DEFAULT NULL,
  `volume_issue` varchar(100) DEFAULT NULL,
  `citation_details` text DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `section_c_research_guidance`
--

CREATE TABLE `section_c_research_guidance` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `scholar_name` varchar(255) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `award_date` date DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_c_research_guidance`
--

INSERT INTO `section_c_research_guidance` (`id`, `faculty_id`, `scholar_name`, `registration_date`, `role`, `status`, `award_date`, `marks`) VALUES
(1, 1, 'shabnam', '2025-07-06', 'Co-Supervisor', 'Submitted', '2025-10-16', 10);

-- --------------------------------------------------------

--
-- Table structure for table `section_d_answer_sheets`
--

CREATE TABLE `section_d_answer_sheets` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `odd` int(11) DEFAULT NULL,
  `even` int(11) DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_d_answer_sheets`
--

INSERT INTO `section_d_answer_sheets` (`id`, `faculty_id`, `odd`, `even`, `marks`) VALUES
(1, 1, 15, 25, 2),
(2, 1, 120, 80, 10);

-- --------------------------------------------------------

--
-- Table structure for table `section_d_institutional_activity`
--

CREATE TABLE `section_d_institutional_activity` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `activity_details` text DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_d_institutional_activity`
--

INSERT INTO `section_d_institutional_activity` (`id`, `faculty_id`, `activity_details`, `marks`) VALUES
(1, 1, 'Member of Proctorial Board and Training & Placement Committee.\r\nActively involved in student grievance handling and placement coordination.\r\n', 12);

-- --------------------------------------------------------

--
-- Table structure for table `section_d_invigilation`
--

CREATE TABLE `section_d_invigilation` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `odd` int(11) DEFAULT NULL,
  `even` int(11) DEFAULT NULL,
  `marks` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_d_invigilation`
--

INSERT INTO `section_d_invigilation` (`id`, `faculty_id`, `odd`, `even`, `marks`) VALUES
(1, 1, 2, 5, 7);

-- --------------------------------------------------------

--
-- Table structure for table `section_e_books`
--

CREATE TABLE `section_e_books` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `year_publication` int(11) DEFAULT NULL,
  `co_authors` varchar(255) DEFAULT NULL,
  `marks` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_e_books`
--

INSERT INTO `section_e_books` (`id`, `faculty_id`, `title`, `publisher`, `year_publication`, `co_authors`, `marks`) VALUES
(1, 1, 'Introduction to Data Science', NULL, NULL, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `section_e_consultancy`
--

CREATE TABLE `section_e_consultancy` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `consultancy_type` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `agency` varchar(255) DEFAULT NULL,
  `duration` varchar(100) DEFAULT NULL,
  `grant_amount` float DEFAULT NULL,
  `remark` text DEFAULT NULL,
  `marks` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_e_consultancy`
--

INSERT INTO `section_e_consultancy` (`id`, `faculty_id`, `consultancy_type`, `title`, `agency`, `duration`, `grant_amount`, `remark`, `marks`) VALUES
(1, 1, NULL, 'ERP System', NULL, NULL, 50000, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `section_e_other`
--

CREATE TABLE `section_e_other` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `activity_details` text DEFAULT NULL,
  `marks` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_e_other`
--

INSERT INTO `section_e_other` (`id`, `faculty_id`, `activity_details`, `marks`) VALUES
(1, 1, 'Mentored students for Smart India Hackathon and actively participated in Clean Campus initiative.\r\nMarks: 4\r\n', 5);

-- --------------------------------------------------------

--
-- Table structure for table `section_e_rd`
--

CREATE TABLE `section_e_rd` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `pi_name` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `agency` varchar(255) DEFAULT NULL,
  `sanction_order` varchar(100) DEFAULT NULL,
  `year_start` int(11) DEFAULT NULL,
  `year_completion` int(11) DEFAULT NULL,
  `total_grant` float DEFAULT NULL,
  `amount_released` float DEFAULT NULL,
  `marks` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_e_rd`
--

INSERT INTO `section_e_rd` (`id`, `faculty_id`, `pi_name`, `title`, `agency`, `sanction_order`, `year_start`, `year_completion`, `total_grant`, `amount_released`, `marks`) VALUES
(1, 1, NULL, 'AI based Attendance System', NULL, NULL, NULL, NULL, NULL, 150000, 5);

-- --------------------------------------------------------

--
-- Table structure for table `section_e_swayam`
--

CREATE TABLE `section_e_swayam` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) DEFAULT NULL,
  `programme_name` varchar(255) DEFAULT NULL,
  `duration_weeks` int(11) DEFAULT NULL,
  `course_name` varchar(255) DEFAULT NULL,
  `fdp_flag` varchar(50) DEFAULT NULL,
  `certification_category` varchar(100) DEFAULT NULL,
  `marks` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `section_e_swayam`
--

INSERT INTO `section_e_swayam` (`id`, `faculty_id`, `programme_name`, `duration_weeks`, `course_name`, `fdp_flag`, `certification_category`, `marks`) VALUES
(1, 1, 'AICTE FDP on Ai', 12, 'java', 'yes', 'Elite / Silver / Gold', 15);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role` enum('faculty','admin','hod','principal') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`) VALUES
(1, 'Riya Singh', 'riya@college.com', '12345', 'faculty'),
(2, 'Dr Sharma', 'hod@college.com', '12345', 'hod'),
(3, 'Principal', 'principal@college.com', '12345', 'principal'),
(4, 'Shivangi Thakur', 'shibu@college.com', '12345', 'faculty');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `acr_approval`
--
ALTER TABLE `acr_approval`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `faculty_profile`
--
ALTER TABLE `faculty_profile`
  ADD PRIMARY KEY (`faculty_id`);

--
-- Indexes for table `section_a_projects`
--
ALTER TABLE `section_a_projects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_a_workload`
--
ALTER TABLE `section_a_workload`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_b_feedback`
--
ALTER TABLE `section_b_feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_b_mentoring`
--
ALTER TABLE `section_b_mentoring`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_b_records`
--
ALTER TABLE `section_b_records`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_b_result`
--
ALTER TABLE `section_b_result`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_c_department_activity`
--
ALTER TABLE `section_c_department_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_c_fdp`
--
ALTER TABLE `section_c_fdp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_c_lab_development`
--
ALTER TABLE `section_c_lab_development`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_c_publications`
--
ALTER TABLE `section_c_publications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_c_research_guidance`
--
ALTER TABLE `section_c_research_guidance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_d_answer_sheets`
--
ALTER TABLE `section_d_answer_sheets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_d_institutional_activity`
--
ALTER TABLE `section_d_institutional_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_d_invigilation`
--
ALTER TABLE `section_d_invigilation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- Indexes for table `section_e_books`
--
ALTER TABLE `section_e_books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `section_e_consultancy`
--
ALTER TABLE `section_e_consultancy`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `section_e_other`
--
ALTER TABLE `section_e_other`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `section_e_rd`
--
ALTER TABLE `section_e_rd`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `section_e_swayam`
--
ALTER TABLE `section_e_swayam`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `acr_approval`
--
ALTER TABLE `acr_approval`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `section_a_projects`
--
ALTER TABLE `section_a_projects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `section_a_workload`
--
ALTER TABLE `section_a_workload`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `section_b_feedback`
--
ALTER TABLE `section_b_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `section_b_mentoring`
--
ALTER TABLE `section_b_mentoring`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `section_b_records`
--
ALTER TABLE `section_b_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `section_b_result`
--
ALTER TABLE `section_b_result`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `section_c_department_activity`
--
ALTER TABLE `section_c_department_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_c_fdp`
--
ALTER TABLE `section_c_fdp`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_c_lab_development`
--
ALTER TABLE `section_c_lab_development`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_c_publications`
--
ALTER TABLE `section_c_publications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `section_c_research_guidance`
--
ALTER TABLE `section_c_research_guidance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_d_answer_sheets`
--
ALTER TABLE `section_d_answer_sheets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `section_d_institutional_activity`
--
ALTER TABLE `section_d_institutional_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_d_invigilation`
--
ALTER TABLE `section_d_invigilation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_e_books`
--
ALTER TABLE `section_e_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_e_consultancy`
--
ALTER TABLE `section_e_consultancy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_e_other`
--
ALTER TABLE `section_e_other`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_e_rd`
--
ALTER TABLE `section_e_rd`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `section_e_swayam`
--
ALTER TABLE `section_e_swayam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `department`
--
ALTER TABLE `department`
  ADD CONSTRAINT `department_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_a_projects`
--
ALTER TABLE `section_a_projects`
  ADD CONSTRAINT `section_a_projects_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_a_workload`
--
ALTER TABLE `section_a_workload`
  ADD CONSTRAINT `section_a_workload_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_b_feedback`
--
ALTER TABLE `section_b_feedback`
  ADD CONSTRAINT `section_b_feedback_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_b_mentoring`
--
ALTER TABLE `section_b_mentoring`
  ADD CONSTRAINT `section_b_mentoring_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_b_records`
--
ALTER TABLE `section_b_records`
  ADD CONSTRAINT `section_b_records_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_b_result`
--
ALTER TABLE `section_b_result`
  ADD CONSTRAINT `section_b_result_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_c_department_activity`
--
ALTER TABLE `section_c_department_activity`
  ADD CONSTRAINT `section_c_department_activity_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_c_fdp`
--
ALTER TABLE `section_c_fdp`
  ADD CONSTRAINT `section_c_fdp_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_c_lab_development`
--
ALTER TABLE `section_c_lab_development`
  ADD CONSTRAINT `section_c_lab_development_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_c_publications`
--
ALTER TABLE `section_c_publications`
  ADD CONSTRAINT `section_c_publications_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_c_research_guidance`
--
ALTER TABLE `section_c_research_guidance`
  ADD CONSTRAINT `section_c_research_guidance_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_d_answer_sheets`
--
ALTER TABLE `section_d_answer_sheets`
  ADD CONSTRAINT `section_d_answer_sheets_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_d_institutional_activity`
--
ALTER TABLE `section_d_institutional_activity`
  ADD CONSTRAINT `section_d_institutional_activity_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `section_d_invigilation`
--
ALTER TABLE `section_d_invigilation`
  ADD CONSTRAINT `section_d_invigilation_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
