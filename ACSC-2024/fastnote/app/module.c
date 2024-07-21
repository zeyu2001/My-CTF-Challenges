// emcc -s WASM=1 -s EXPORTED_RUNTIME_METHODS='["cwrap", "addFunction"]' -s ALLOW_TABLE_GROWTH module.c --no-entry -o module.js
#include <emscripten.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct note {
  char *(*toHTML) (char *title, char *content);
  struct note *next;
  char *title;
  char *content;
} note;

note *head = NULL;

char *sanitize(char *str) {
  char *safe = malloc(strlen(str) * 6);
  safe[0] = '\0';
  
  while (*str) {
    switch (*str) {
      case '<':
        strcat(safe, "&lt;");
        break;
      case '>':
        strcat(safe, "&gt;");
        break;
      case '&':
        strcat(safe, "&amp;");
        break;
      case '"':
        strcat(safe, "&quot;");
        break;
      case '\'':
        strcat(safe, "&#x27;");
        break;
      default:
        strncat(safe, str, 1);
        break;
    }
    str++;
  }
  return safe;
}

char *toSafeHTML(char *title, char *content) {
  int length = strlen(title) + strlen(content) + 100;
  char *safeHTML = malloc(length);
  safeHTML[0] = '\0';

  char *safeTitle = sanitize(title);
  char *safeContent = sanitize(content);

  snprintf(safeHTML, length, "<article><h1>%s</h1><p>%s</p></article>", safeTitle, safeContent);
  return safeHTML;
}

EMSCRIPTEN_KEEPALIVE
int addNote(char *title, char *content) {

  if (strlen (title) > 65 || strlen (content) > 100) {
    return -1;
  }

  char *noteTitle = malloc(strlen(title) + 1);
  char *noteContent = malloc(strlen(content) + 1);

  strcpy(noteTitle, title);
  strcpy(noteContent, content);
  struct note *n = malloc(sizeof(struct note));
  n->title = noteTitle;
  n->content = noteContent;
  n->toHTML = toSafeHTML;
  n->next = NULL;

  if (head == NULL) {
    head = n;
    return 0;
  }

  int i = 0;
  note *current = head;
  while (current->next != NULL) {
    current = current->next;
    i++;
  }
  current->next = n;
  return i + 1;
}

EMSCRIPTEN_KEEPALIVE
void populateNoteHTML(int *(*callback)(char *, int)) {
  int i = 0;
  note *current = head;
  while (current != NULL) {
    callback(current->toHTML(current->title, current->content), i);
    current = current->next;
    i++;
  }
}

EMSCRIPTEN_KEEPALIVE
int deleteNote(int idx, void (*callback)(int)) {
  note *current = head;
  note *prev = head;

  int i = 0;
  while (current != NULL) {
    if (i == idx) {
      prev->next = current->next;
      free(current);
      callback(idx);
      return 0;
    }
    prev = current;
    current = current->next;
    i++;
  }
  
  return -1;
}