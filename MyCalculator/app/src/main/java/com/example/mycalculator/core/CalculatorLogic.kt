package com.example.mycalculator.core

import java.text.DecimalFormat
import java.text.DecimalFormatSymbols
import java.util.Locale
import kotlin.math.sqrt

// DISCLAIMER: This parser handles precedence for * and / over + and -.
// It does NOT handle parentheses.
// It includes basic handling for leading negative numbers and some cases of negative numbers in expressions.

/**
 * Calculates the result of a mathematical expression string.
 * Handles basic arithmetic operations (+, -, *, /) with precedence for * and /.
 * Does not support parentheses.
 * Includes preprocessing for unary minus and combined operators.
 *
 * @return A string representing the calculated result or an error message.
 */
fun String.calculate(): String {
    return try {
        var currentExpression = this.trim().replace(" ", "")

        // Preprocessing steps:
        // 1. Handle leading unary minus: "-5+2" becomes "0-5+2"
        if (currentExpression.startsWith("-")) {
            currentExpression = "0$currentExpression"
        }

        // 2. Normalize combined operators to assist the splitting logic:
        //    "5*-2" becomes "5*0-2"
        //    "5/-2" becomes "5/0-2"
        //    "5+-2" becomes "5+0-2"
        //    "5--2" becomes "5-0-2" (or "5+2" if direct simplification is preferred,
        //                            but "5-0-2" is consistent with other patterns here
        //                            and the consolidation logic in evaluateOperations
        //                            should handle it correctly).
        currentExpression = currentExpression.replace("*-", "*0-")
        currentExpression = currentExpression.replace("/-", "/0-")
        currentExpression = currentExpression.replace("+-", "+0-")
        currentExpression = currentExpression.replace("--", "-0-") // Or currentExpression.replace("--", "+")

        // --- Pass 1: Perform Multiplication and Division ---
        currentExpression = evaluateOperations(currentExpression, listOf("*", "/"))

        // --- Pass 2: Perform Addition and Subtraction ---
        currentExpression = evaluateOperations(currentExpression, listOf("+", "-"))

        // After all operations, the result should ideally be a single number.
        // Final validation and formatting:
        val finalResult = currentExpression.toDoubleOrNull()
        if (finalResult != null) {
            finalResult.formatToString() // Use the renamed extension function
        } else if (currentExpression.contains(Regex("[*/+\\-]")) &&
            currentExpression.length > 1 &&
            !isNumeric(currentExpression)) {
            // If operators still exist and it's not a simple negative number,
            // the expression is likely invalid or malformed.
            "Error: Invalid expression"
        } else {
            // Attempt to parse again. It might be a single number that
            // didn't go through extensive operations, or a valid negative number.
            currentExpression.toDoubleOrNull()?.formatToString() ?: "Error: Invalid format"
        }

    } catch (e: ArithmeticException) {
        "Error: ${e.message}" // e.g., "Error: Division by zero"
    } catch (e: NumberFormatException) {
        "Error: Invalid number format" // From toDoubleOrNull failures or explicit throws
    } catch (e: IllegalStateException) {
        "Error: ${e.message}" // From evaluateOperations if logic fails (e.g., operator in invalid position)
    } catch (e: Exception) {
        // Log for debugging purposes:
        // android.util.Log.e("CalculatorLogic", "Unexpected error: ${e.message}", e)
        "Error: Calculation failed" // Generic error for unexpected issues
    }
}

/**
 * Evaluates an expression for a given set of operators (e.g., [* /] or [+ -]).
 * This function processes the expression from left to right, applying the target operators.
 *
 * @param expression The mathematical expression string to evaluate.
 * @param targetOperators A list of operators to process in this pass.
 * @return The expression string after the specified operations have been performed.
 * @throws NumberFormatException if an invalid number is encountered.
 * @throws IllegalStateException if an operator is in an invalid position or unknown.
 * @throws ArithmeticException for division by zero.
 */
private fun evaluateOperations(expression: String, targetOperators: List<String>): String {
    val decimalFormatSymbols = DecimalFormatSymbols(Locale.US) // For formatting intermediate results consistently

    // Regex to split the expression by operators, keeping the operators as tokens.
    // Example: "0-5*0-2" -> ["0", "-", "5", "*", "0", "-", "2"]
    val operatorRegex = Regex("(?<=[*/+\\-])|(?=[*/+\\-])")
    var parts = expression.split(operatorRegex).filter { it.isNotEmpty() }.toMutableList()

    // Consolidate unary minus for numbers.
    // This step ensures that numbers like "-5" are treated as a single token if they appear
    // at the beginning of the 'parts' list or after another operator.
    // Example: if parts are ["-", "5", "+", "2"], tempParts becomes ["-5", "+", "2"]
    // Example: if parts from "0-5" is ["0", "-", "5"], tempParts remains ["0", "-", "5"]
    val consolidatedParts = mutableListOf<String>()
    var j = 0
    while (j < parts.size) {
        if (parts[j] == "-" &&
            (consolidatedParts.isEmpty() || consolidatedParts.last() in listOf("*", "/", "+", "-")) &&
            j + 1 < parts.size &&
            isNumeric(parts[j + 1])) {
            // This is a negative sign for a number (unary minus).
            consolidatedParts.add("-" + parts[j + 1])
            j += 2 // Consumed operator and number
        } else {
            consolidatedParts.add(parts[j])
            j += 1
        }
    }
    parts = consolidatedParts

    var i = 0
    while (i < parts.size) {
        val token = parts[i]
        if (token in targetOperators) {
            val operator = token

            // Check for operator at invalid positions (start/end or missing operands)
            if (i == 0 || i >= parts.size - 1) {
                // If only one part remains and it's a number, processing is done for this pass.
                if (parts.size == 1 && isNumeric(parts[0])) break
                throw IllegalStateException("Operator '$operator' is in an invalid position within '${parts.joinToString("")}'")
            }

            val leftOperandStr = parts[i - 1]
            val rightOperandStr = parts[i + 1]

            val leftOperand = leftOperandStr.toDoubleOrNull()
            val rightOperand = rightOperandStr.toDoubleOrNull()

            if (leftOperand == null) {
                throw NumberFormatException("Invalid left operand '$leftOperandStr' for operator '$operator'")
            }
            if (rightOperand == null) {
                throw NumberFormatException("Invalid right operand '$rightOperandStr' for operator '$operator'")
            }

            val result = when (operator) {
                "*" -> leftOperand * rightOperand
                "/" -> {
                    if (rightOperand == 0.0) throw ArithmeticException("Division by zero")
                    leftOperand / rightOperand
                }
                "+" -> leftOperand + rightOperand
                "-" -> leftOperand - rightOperand
                else -> throw IllegalStateException("Unknown operator: $operator")
            }

            // Format the result before replacing it in the parts list
            val resultFormatted = DecimalFormat("#.##############", decimalFormatSymbols).format(result)
            parts[i - 1] = resultFormatted // Replace left operand with the result
            parts.removeAt(i + 1)          // Remove the right operand
            parts.removeAt(i)              // Remove the operator
            i-- // Adjust index to re-evaluate from the new merged part's position
        } else {
            i++
        }
    }
    return parts.joinToString("")
}

/**
 * Checks if a string represents a valid number (integer or decimal).
 * @param s The string to check.
 * @return True if the string is a valid number, false otherwise.
 */
private fun isNumeric(s: String): Boolean {
    return s.toDoubleOrNull() != null
}

/**
 * Formats a Double to a String representation with up to 14 decimal places,
 * using US locale for consistent decimal point.
 */
private fun Double.formatToString(): String {
    val df = DecimalFormat("#.##############", DecimalFormatSymbols(Locale.US))
    return df.format(this)
}

// --- Standalone Mathematical Helper Functions (can be part of CalculatorLogic or a separate utility) ---

/**
 * Calculates the square root of a number.
 * @param number The number to calculate the square root of.
 * @return The square root of the number.
 * @throws IllegalArgumentException if the number is negative.
 */
fun squareRoot(number: Double): Double {
    if (number < 0) {
        throw IllegalArgumentException("Cannot calculate square root of a negative number.")
    }
    return sqrt(number)
}

/**
 * Converts a number to its percentage (divides by 100) and formats it as a string.
 * @param number The number to convert to a percentage.
 * @return A string representation of the number as a percentage.
 */
fun convertToPercentage(number: Double): String {
    return (number / 100.0).formatToString()
}

/**
 * Calculates the inverse (1/x) of a number.
 * @param number The number to calculate the inverse of.
 * @return The inverse of the number.
 * @throws IllegalArgumentException if the number is zero.
 */
fun inverse(number: Double): Double {
    if (number == 0.0) {
        throw IllegalArgumentException("Cannot divide by zero for inverse operation.")
    }
    return 1.0 / number
}