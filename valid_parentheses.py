class Solution:
    def isValid(self, s: str) -> bool:
        bracket_map = {
            "(":")",
            "[":"]",
            "{":"}"
        }
        chars = list(s)
        back_track_index = len(chars)-1
        for index in range(len(chars)):
            if chars[index] in bracket_map and bracket_map[chars[index]] != chars[back_track_index]:
                return False
            elif chars[index] not in bracket_map:
                return False
            back_track_index -= 1
        return True