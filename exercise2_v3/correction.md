# Fundamentals of Data Engineering – Exercise 2 Correction
### Student: Javier Liarte
---

## Correction Notes

### Issues to solve:

#### (scrapper) Modify get_songs to use catalog (2 points)
- [ ] Points awarded: 1
- [ ] Comments: The scrapper first downloads a catalog into the 'files' directory, but you ar searching the catalog in 'catalogs' directory, so it throws and error as it does not find the file:
```
   catalog = files.load_from_json(Path(f"{output_directory}catalogs/catalog.json"))
    print(catalog)
```
I removed the catalog directory and it works fine.
Also, printing variables without any formatting or large variables, is only for testing, you cant send a final script with that. Same for the commented code in the main.py file. 

#### (scrapper) Check logs for strange messages (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: The thing is that, when downloading the catalog, is where you get the messages. To clarify, the catalog stores the urls from each song, that we use to scrap the web.

#### (cleaner) Avoid processing catalogs (0.5 points)
- [ ] Points awarded: 0.2
- [ ] Comments: You added the catalogs folder to solve that issue. That can be a way. But your implementation hardcoded the folders you want to skip. A better way is to only accept from the 'songs' folder, and only accept '.txt' files.

#### (Validator) Fix directory creation issue (0.5 points)
- [ ] Points awarded: 0.5
- [ ] Comments: Works, but as I say on the previous step, and you say on the doc, is not the best way.

#### (Validator) Additional validation rule (0.5 points)
- [ ] Points awarded: 0.5
- [ ] Comments:

#### Code improvements (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: No code improvements provided.

### Functionalities to add:

#### 'results' module (0.5 points)
- [ ] Points awarded: 0.3
- [ ] Comments: 
- - A single python file is not a module. You should make a directory and put it inside, so you can add libraries and utility functions to it for the main file to call.
- - You are not logging anything here.

#### 'lyrics' module (2 points)
- [ ] Points awarded: 0.5
- [ ] Comments: 
- - A single python file is not a module. You should make a directory and put it inside, so you can add libraries and utility functions to it for the main file to call.
- - The files are stored in the same 'validations/ok' folder, when it should have his own directory.
- - Not working ith all the chord lines. Example output:
```
Quizá fue el sueño de un sureño del sur
Lo que me mantiene en pie
SIm                        FA#m
Llueve y no se cuando escampa
SIm                          LA   FA#m
Tal vez Se empape hasta mi alma
Y en este lado reina la calma Yo siempre voy donde va mi alma
```


#### 'insights' module (2 points)
- [ ] Points awarded: 0
- [ ] Comments: Not implemented

#### Main execution file (1 point)
- [ ] Points awarded: 0
- [ ] Comments: Not implemented

---

## Total Score: 2.8 / 10 points

## General Comments:

This submission has significant issues that prevent most of the pipeline from functioning. While you've attempted to address the required components, implementation problems and missing sections severely limit the functionality.

**Critical Issues:**

1. **Scrapper Module (1/2)**: The catalog path is hardcoded to 'catalogs' directory, but the scrapper downloads to 'files' directory, causing immediate failure. This shows lack of testing before submission. Additionally, debug code (print statements, commented code) remains in the final version.

2. **Implementation Approach**: Hardcoding folder names to skip (catalogs) rather than explicitly selecting what to process (songs/*.txt) is poor programming practice that doesn't scale.

3. **Incomplete Submission**: 
   - Insights module: Not implemented (0/2.0)
   - Main execution file: Not implemented (0/1.0)
   - Code improvements: Not provided (0/0.5)

4. **Module Structure**: Single Python files instead of proper module directories with utilities and dependencies.

**What Partially Works:**
- Validation rule added successfully (0.5/0.5)
- Validator directory fix (0.3/0.5 - not optimal approach)
- Lyrics extraction attempts (0.5/2.0 - chord removal incomplete, wrong directory)
- Results module exists (0.3/0.5 - not a proper module, no logging)

**Missing Throughout:**
- No logging in any module
- No result persistence (only console output)
- Testing was clearly not performed

**For Future Success:**
This low score (2.8/10) reflects that the majority of the exercise was not completed or doesn't work. Before any submission:
1. **Test every module individually and together**
2. **Complete all required components** - half-finished work gets minimal credit
3. **Remove debug code** (print statements, comments) from final submissions
4. **Follow existing patterns** in the codebase for structure and conventions
5. **Ask for help** when stuck rather than submitting incomplete work

The parts you attempted show you have some understanding, but execution and completion are critical for passing grades.
