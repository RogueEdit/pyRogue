from typing import List, Dict, Tuple
import random

# Constants from your existing code
eggConstant: int = 1073741824

def getIDBoundarys(tier: int) -> Tuple[int, int]:
    """
    Get the ID bounds for a given tier.

    Args:
        tier (int): The tier index.

    Returns:
        Tuple[int, int]: A tuple containing the start and end IDs.
    """
    # Calculate the start and end IDs for the given tier
    start: int = tier * eggConstant
    end: int = (tier + 1) * eggConstant - 1
    return max(start, 255), end

def generateRandomID(start: int, end: int, manaphy: bool = False) -> int:
    """
    Get a random ID within the given range.

    Args:
        start (int): The start of the ID range.
        end (int): The end of the ID range.
        manaphy (bool): Whether the ID is for a Manaphy egg.

    Returns:
        int: The random ID.
    """
    if manaphy:
        # Generate a random ID that is divisible by 204 within the specified range
        return random.randrange(start // 204 * 204, (end // 204 + 1) * 204, 204)

    # Generate a regular random ID within the specified range
    result: int = random.randint(start, end)

    if result % 204 == 0:
        result -= 1

    return max(result, 1)

def validate_egg_generation(num_samples: int, isManaphy: bool, tier: int, eggAmount: int) -> int:
    """
    Validate the egg ID generation against the criteria.

    Args:
        num_samples (int): Number of samples to generate and validate.
        isManaphy (bool): Whether the eggs are Manaphy eggs.
        tier (int): Tier index for the eggs.
        eggAmount (int): Number of eggs to generate.

    Returns:
        int: Number of matches that meet the criteria.
    """
    match_count = 0
    start, end = getIDBoundarys(0 if isManaphy else tier)

    for _ in range(eggAmount):
        eggID: int = generateRandomID(start, end, isManaphy)

        # Check if the generated ID meets the criteria
        if eggID % 204 == 0:
            match_count += 1

    return match_count

if __name__ == "__main__":
    # Define parameters for validation
    num_samples = 100
    isManaphy = False  # Change to True if validating Manaphy eggs
    tier = 2            # Example tier index for eggs
    eggAmount = 100     # Number of eggs to generate and validate

    # Perform validation
    matches = validate_egg_generation(num_samples, isManaphy, tier, eggAmount)

    # Print results
    print(f"Out of {num_samples} samples, {matches} matched the criteria.")
